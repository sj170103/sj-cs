import os
import sys
import datetime
import subprocess

def install_pyaudio_if_needed():
    """pyaudio가 설치되어 있는지 확인하고, 없으면 설치한다."""
    try:
        import pyaudio
    except ImportError:
        print('pyaudio가 설치되어 있지 않습니다. 설치를 시작합니다...')
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyaudio'])
            print('pyaudio 설치가 완료되었습니다.')
        except subprocess.CalledProcessError:
            print('pyaudio 설치에 실패했습니다. 수동으로 설치해 주세요.')
            sys.exit(1)

def get_current_timestamp():
    """현재 날짜 및 시간을 ‘년월일-시간분초’ 형식으로 반환한다."""
    now = datetime.datetime.now()
    return now.strftime('%Y%m%d-%H%M%S')

def create_records_directory():
    """녹음 파일 저장을 위한 records 폴더를 생성한다."""
    if not os.path.exists('records'):
        os.makedirs('records')

def record_voice(seconds=5):
    """마이크로부터 음성을 녹음하여 WAV 파일로 저장한다."""
    import pyaudio
    import wave

    chunk = 1024
    format = pyaudio.paInt16
    channels = 1
    rate = 44100
    record_seconds = seconds
    timestamp = get_current_timestamp()
    filename = 'records/' + timestamp + '.wav'

    audio = pyaudio.PyAudio()

    print('녹음을 시작합니다...')

    stream = audio.open(format=format,
                        channels=channels,
                        rate=rate,
                        input=True,
                        frames_per_buffer=chunk)

    frames = []

    for _ in range(0, int(rate / chunk * record_seconds)):
        data = stream.read(chunk)
        frames.append(data)

    print('녹음이 완료되었습니다:', filename)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(audio.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()

def list_records_by_date_range(start_date_str, end_date_str):
    """입력된 날짜 범위 내의 녹음 파일 목록을 출력한다."""
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

def main():
    """메인 실행 함수"""
    install_pyaudio_if_needed()
    create_records_directory()

    print('\n메뉴:')
    print('1. 음성 녹음')
    print('2. 녹음 파일 날짜별 조회')
    choice = input('선택 (1 또는 2): ')

    if choice == '1':
        sec = input('녹음 시간(초, 기본 5초): ')
        try:
            sec = int(sec)
        except ValueError:
            sec = 5
        record_voice(seconds=sec)
    elif choice == '2':
        start = input('시작 날짜 (YYYYMMDD): ')
        end = input('종료 날짜 (YYYYMMDD): ')
        list_records_by_date_range(start, end)
    else:
        print('잘못된 선택입니다. 프로그램을 종료합니다.')

if __name__ == '__main__':
    main()
