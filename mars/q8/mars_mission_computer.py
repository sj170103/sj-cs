import platform  # OS, CPU 정보 조회용
import os  # CPU 코어 수 조회용
import json  # JSON 출력용
import subprocess  # pip 설치 실행용
import sys  # 파이썬 실행 경로 확인용

# 시스템정보를 가져올때 쓰는 라이브러리 최신안정화버전 자동설치후 import
try:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'psutil'])
except subprocess.CalledProcessError:
    print("설치 실패 프로그램 종료")
    sys.exit(1)


class MissionComputer:
    def __init__(self):
        self.info_items = []  # 시스템 정보 항목 리스트
        self.load_items = []  # 시스템 부하 항목 리스트
        self.load_setting()  # setting.txt 읽기

    def load_setting(self):
        try:
            with open('setting.txt', 'r') as f:
                lines = f.readlines()
                for line in lines:
                    key, value = line.strip().split('=')
                    if key == 'info':
                        self.info_items = value.split(',')
                    elif key == 'load':
                        self.load_items = value.split(',')
        except Exception:
            self.info_items = ['os', 'os_version', 'cpu', 'cpu_core', 'memory']
            self.load_items = ['cpu_usage', 'memory_usage']

    def get_mission_computer_info(self):
        try:
            info = {}

            if 'os' in self.info_items:
                info['os'] = platform.system()
            if 'os_version' in self.info_items:
                info['os_version'] = platform.version()
            if 'cpu' in self.info_items:
                info['cpu'] = platform.processor()
            if 'cpu_core' in self.info_items:
                info['cpu_core'] = os.cpu_count()
            if 'memory' in self.info_items:
                info['memory'] = str(round(psutil.virtual_memory().total / (1024 * 1024), 2)) + ' MB'

            print('Mission Computer Info:', json.dumps(info, indent=4))

        except Exception as e:
            print('시스템 정보 조회 실패:', e)

    def get_mission_computer_load(self):
        try:
            load = {}

            if 'cpu_usage' in self.load_items:
                load['cpu_usage'] = str(psutil.cpu_percent(interval=1)) + ' %'
            if 'memory_usage' in self.load_items:
                load['memory_usage'] = str(psutil.virtual_memory().percent) + ' %'

            print('Mission Computer Load:', json.dumps(load, indent=4))

        except Exception as e:
            print('시스템 부하 조회 실패:', e)


# 객체 생성
runComputer = MissionComputer()

# 시스템 정보 출력
runComputer.get_mission_computer_info()

# 시스템 부하 정보 출력
runComputer.get_mission_computer_load()
