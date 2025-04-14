import os
import sys
import platform
import random
import json
import time
import subprocess

# psutil 설치 및 예외처리
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


class DummySensor:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0.0,
            'mars_base_external_temperature': 0.0,
            'mars_base_internal_humidity': 0.0,
            'mars_base_external_illuminance': 0.0,
            'mars_base_internal_co2': 0.0,
            'mars_base_internal_oxygen': 0.0
        }

    def set_env(self):
        self.env_values['mars_base_internal_temperature'] = random.uniform(18, 30)
        self.env_values['mars_base_external_temperature'] = random.uniform(0, 21)
        self.env_values['mars_base_internal_humidity'] = random.uniform(50, 60)
        self.env_values['mars_base_external_illuminance'] = random.uniform(500, 715)
        self.env_values['mars_base_internal_co2'] = random.uniform(0.02, 0.1)
        self.env_values['mars_base_internal_oxygen'] = random.uniform(4, 7)

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


class MissionComputer(DummySensor):
    def __init__(self):
        super().__init__()
        self.settings = self.load_settings()

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


if __name__ == '__main__':
    runComputer = MissionComputer()

    runComputer.set_env()
    env_data = runComputer.get_env()

    print('[현재 센서 데이터]')
    for key, value in env_data.items():
        print(f'{key}: {value:.2f}')

    runComputer.get_mission_computer_info()
    runComputer.get_mission_computer_load()
