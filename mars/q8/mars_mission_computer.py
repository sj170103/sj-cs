# ----------------------------------------
# [1] 필요한 모듈 import
# - 시스템 정보 수집
# - 센서 값 랜덤 생성
# - JSON 출력
# - psutil 없으면 자동설치 처리
# ----------------------------------------
import os
import sys
import platform
import random
import json
import time
import subprocess

# 시스템 상태 정보를 수집하기 위한 라이브러리(psutil)
# 없을 경우 자동 설치 처리
try:
    import psutil
except ImportError:
    print('psutil 모듈 없음 → 설치 시도')
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'psutil'])
        import psutil
    except subprocess.CalledProcessError:
        print('psutil 설치 실패 → 프로그램 종료')
        sys.exit(1)


# ----------------------------------------
# [2] DummySensor 클래스 (문제7 기능)
# - 센서값 랜덤 생성
# - 로그 파일 기록
# ----------------------------------------
class DummySensor:
    def __init__(self):
        # 센서 초기값 (0으로 초기화)
        self.env_values = {
            'mars_base_internal_temperature': 0.0,
            'mars_base_external_temperature': 0.0,
            'mars_base_internal_humidity': 0.0,
            'mars_base_external_illuminance': 0.0,
            'mars_base_internal_co2': 0.0,
            'mars_base_internal_oxygen': 0.0
        }

    # 랜덤한 센서값 생성
    def set_env(self):
        self.env_values['mars_base_internal_temperature'] = random.uniform(18, 30)
        self.env_values['mars_base_external_temperature'] = random.uniform(0, 21)
        self.env_values['mars_base_internal_humidity'] = random.uniform(50, 60)
        self.env_values['mars_base_external_illuminance'] = random.uniform(500, 715)
        self.env_values['mars_base_internal_co2'] = random.uniform(0.02, 0.1)
        self.env_values['mars_base_internal_oxygen'] = random.uniform(4, 7)

    # 센서값 리턴 + 파일 로그 저장
    def get_env(self):
        log_line = '{time}, {internal_temp:.2f}, {external_temp:.2f}, {humidity:.2f}, {illuminance:.2f}, {co2:.4f}, {oxygen:.2f}\n'.format(
            time=time.strftime('%Y-%m-%d %H:%M:%S'),
            internal_temp=self.env_values['mars_base_internal_temperature'],
            external_temp=self.env_values['mars_base_external_temperature'],
            humidity=self.env_values['mars_base_internal_humidity'],
            illuminance=self.env_values['mars_base_external_illuminance'],
            co2=self.env_values['mars_base_internal_co2'],
            oxygen=self.env_values['mars_base_internal_oxygen']
        )

        with open('sensor_log.txt', 'a') as file:
            file.write(log_line)

        return self.env_values


# ----------------------------------------
# [3] MissionComputer 클래스 (문제8 핵심)
# - DummySensor 상속
# - 시스템 상태정보 출력 기능 추가
# - 부하정보 출력 기능 추가
# - setting.txt로 출력 항목 선택 가능
# ----------------------------------------
class MissionComputer(DummySensor):
    def __init__(self):
        super().__init__()  # DummySensor 초기화
        self.settings = self.load_settings()  # setting.txt 항목 로딩

    # setting.txt 파일을 읽어 출력 항목 지정
    def load_settings(self):
        settings = []
        try:
            with open('setting.txt', 'r') as f:
                for line in f:
                    line = line.strip()
                    if line != '':
                        settings.append(line)
        except FileNotFoundError:
            print('setting.txt 없음 → 전체 항목 출력')
            settings = [
                'OS', 'OS Version', 'CPU Type', 'CPU Core Count',
                'Memory Total', 'Memory Usage', 'CPU Usage'
            ]
        return settings

    # 시스템 주요 정보 출력
    def get_mission_computer_info(self):
        try:
            info = {
                'OS': platform.system(),
                'OS Version': platform.version(),
                'CPU Type': platform.processor(),
                'CPU Core Count': os.cpu_count(),
                'Memory Total': psutil.virtual_memory().total,
                'Memory Usage': psutil.virtual_memory().percent,
                'CPU Usage': psutil.cpu_percent(interval=1)
            }

            output = {key: value for key, value in info.items() if key in self.settings}

            print('[미션 컴퓨터 정보]')
            print(json.dumps(output, indent=4, ensure_ascii=False))

        except Exception as e:
            print('시스템 정보 조회 중 오류 발생:', e)

    # 시스템 부하 정보 출력
    def get_mission_computer_load(self):
        try:
            load = {
                'CPU Usage': psutil.cpu_percent(interval=1),
                'Memory Usage': psutil.virtual_memory().percent
            }

            output = {key: value for key, value in load.items() if key in self.settings}

            print('[미션 컴퓨터 부하 정보]')
            print(json.dumps(output, indent=4, ensure_ascii=False))

        except Exception as e:
            print('시스템 부하 조회 중 오류 발생:', e)


# ----------------------------------------
# [4] 프로그램 실행 부분
# - MissionComputer 객체 생성
# - 센서값 생성 및 출력
# - 시스템 정보 및 부하 정보 출력
# ----------------------------------------
if __name__ == '__main__':
    runComputer = MissionComputer()

    runComputer.set_env()  # 센서값 랜덤 생성
    env_data = runComputer.get_env()  # 센서값 출력 및 로그 기록

    print('[현재 센서 데이터]')
    for key, value in env_data.items():
        print(f'{key}: {value:.2f}')

    runComputer.get_mission_computer_info()  # 시스템 정보 출력
    runComputer.get_mission_computer_load()  # 시스템 부하 출력
