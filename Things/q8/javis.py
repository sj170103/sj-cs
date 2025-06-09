import os
import sys
import subprocess
import importlib
import datetime
import wave
import csv

def install_required_libraries():
    """필수 라이브러리(pyaudio, speech_recognition, pydub) 설치 확인 및 자동 설치"""
    def install_package(package):
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f'{package} 설치 완료')
        except subprocess.CalledProcessError:
            print(f'{package} 설치 실패. 수동 설치가 필요합니다.')
            sys.exit(1)

    required_packages = {
        'pyaudio': 'pyaudio',
        'speech_recognition': 'SpeechRecognition',
        'pydub': 'pydub'
    }

    for module_name, pip_name in required_packages.items():
        try:
            importlib.import_module(module_name)
        except ImportError:
            print(f'{pip_name}가 설치되어 있지 않습니다. 설치를 시작합니다...')
            install_package(pip_name)

    check_ffmpeg_installed()

def check_ffmpeg_installed():
    """시스템에 ffmpeg가 설치되어 있는지 확인한다 (pydub 사용 시 필요)"""
    try:
        subprocess.check_output(['ffmpeg', '-version'])
        print('ffmpeg 설치 확인 완료')
    except (subprocess.CalledProcessError, FileNotFoundError):
        print('ffmpeg가 시스템에 설치되어 있지 않습니다.')
        print('pydub를 사용하려면 ffmpeg를 설치해야 합니다.')
        print('설치 방법 예시:')
        print(' - Windows: https://ffmpeg.org/download.html')
        print(' - Mac: brew install ffmpeg')
        print(' - Ubuntu: sudo apt install ffmpeg')
        sys.exit(1)

def get_current_timestamp():
    now = datetime.datetime.now()
    return now.strftime('%Y%m%d-%H%M%S')

def create_records_directory():
    if not os.path.exists('records'):
        os.makedirs('records')

def record_voice(seconds=5):
    import pyaudio
    chunk = 1024
    format = pyaudio.paInt16
    channels = 1
    rate = 44100
    filename = 'records/' + get_current_timestamp() + '.wav'

    audio = pyaudio.PyAudio()
    print('녹음을 시작합니다...')

    stream = audio.open(format=format,
                        channels=channels,
                        rate=rate,
                        input=True,
                        frames_per_buffer=chunk)

    frames = []
    for _ in range(0, int(rate / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    print('녹음이 완료되었습니다:', filename)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))

def list_records_by_date_range(start_date_str, end_date_str):
    try:
        start_date = datetime.datetime.strptime(start_date_str, '%Y%m%d')
        end_date = datetime.datetime.strptime(end_date_str, '%Y%m%d')
    except ValueError:
        print('날짜 형식 오류: YYYYMMDD 형식으로 입력하세요.')
        return

    if not os.path.exists('records'):
        print('records 폴더가 존재하지 않습니다.')
        return

    print(f'{start_date_str} ~ {end_date_str} 사이의 녹음 파일 목록:')
    found = False
    for filename in sorted(os.listdir('records')):
        if filename.endswith('.wav'):
            try:
                file_date_str = filename.split('-')[0]
                file_date = datetime.datetime.strptime(file_date_str, '%Y%m%d')
                if start_date <= file_date <= end_date:
                    print('-', filename)
                    found = True
            except Exception:
                continue
    if not found:
        print('해당 날짜 범위에 녹음 파일이 없습니다.')

def transcribe_audio_to_csv(filename):
    import speech_recognition as sr
    from pydub import AudioSegment

    filepath = os.path.join('records', filename)
    base = os.path.splitext(filepath)[0]
    csv_filename = base + '.csv'

    recognizer = sr.Recognizer()
    print('STT 변환 중:', filename)

    try:
        with sr.AudioFile(filepath) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language='ko-KR')

        duration = AudioSegment.from_wav(filepath).duration_seconds
        with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Time', 'Text'])
            writer.writerow(['0~{:.1f}s'.format(duration), text])

        print('CSV 저장 완료:', os.path.basename(csv_filename))

    except sr.UnknownValueError:
        print('음성을 이해할 수 없습니다:', filename)
        with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Time', 'Text'])
            writer.writerow(['-', ''])  # 빈 텍스트 저장
        print('빈 CSV 저장 완료:', os.path.basename(csv_filename))

    except Exception as e:
        print('오류 발생:', str(e))

def transcribe_all_wav_files():
    if not os.path.exists('records'):
        print('records 폴더가 존재하지 않습니다.')
        return
    for f in os.listdir('records'):
        if f.endswith('.wav'):
            transcribe_audio_to_csv(f)

def search_keyword_in_transcripts(keyword):
    found = False
    for f in os.listdir('records'):
        if f.endswith('.csv'):
            with open(os.path.join('records', f), 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader, None)
                for row in reader:
                    if keyword in row[1]:
                        print('[{}] {}: {}'.format(f, row[0], row[1]))
                        found = True
    if not found:
        print('검색된 결과가 없습니다.')

def main():
    install_required_libraries()
    create_records_directory()

    while True:
        print('\n메뉴:')
        print('1. 음성 녹음')
        print('2. 녹음 파일 날짜별 조회')
        print('3. STT 변환 및 CSV 저장')
        print('4. 키워드 검색 (보너스)')
        print('5. 종료')
        choice = input('선택 (1~5): ')

        if choice == '1':
            try:
                sec = int(input('녹음 시간 (초, 기본 5초): '))
            except ValueError:
                sec = 5
            record_voice(seconds=sec)
        elif choice == '2':
            start = input('시작 날짜 (YYYYMMDD): ')
            end = input('종료 날짜 (YYYYMMDD): ')
            list_records_by_date_range(start, end)
        elif choice == '3':
            transcribe_all_wav_files()
        elif choice == '4':
            keyword = input('검색할 키워드를 입력하세요: ')
            search_keyword_in_transcripts(keyword)
        elif choice == '5':
            print('프로그램을 종료합니다.')
            break
        else:
            print('잘못된 선택입니다.')

if __name__ == '__main__':
    main()
