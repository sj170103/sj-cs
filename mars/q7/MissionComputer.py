import time

# DummySensor 클래스
# 문제 3에서 제작한 센서 시뮬레이션 클래스
# 센서 데이터를 무작위로 생성하여 env_values 딕셔너리에 저장하고 반환
class DummySensor:
    def __init__(self):
        # 센서가 측정할 환경값들을 저장하는 딕셔너리
        self.env_values = {
            'mars_base_internal_temperature': 0.0,
            'mars_base_external_temperature': 0.0,
            'mars_base_internal_humidity': 0.0,
            'mars_base_external_illuminance': 0.0,
            'mars_base_internal_co2': 0.0,
            'mars_base_internal_oxygen': 0.0
        }

    # 센서값을 무작위로 설정 (time.time() % 1 사용)
    def set_env(self):
        t = time.time() % 1  # 0 ~ 1 사이의 소수값
        self.env_values['mars_base_internal_temperature'] = 18 + (12 * t)
        self.env_values['mars_base_external_temperature'] = 0 + (21 * t)
        self.env_values['mars_base_internal_humidity'] = 50 + (10 * t)
        self.env_values['mars_base_external_illuminance'] = 500 + (215 * t)
        self.env_values['mars_base_internal_co2'] = 0.02 + (0.08 * t)
        self.env_values['mars_base_internal_oxygen'] = 4 + (3 * t)

    # 센서 데이터를 반환 (env_values 딕셔너리)
    def get_env(self):
        self.set_env()
        return self.env_values


# MissionComputer 클래스
# 센서 데이터를 받아 저장하고, 주기적으로 출력하는 컴퓨터 역할
class MissionComputer:
    def __init__(self, ds):
        self.ds = ds  # 외부에서 전달받은 DummySensor 인스턴스
        # 현재 측정된 환경값 저장용 딕셔너리
        self.env_values = {key: 0.0 for key in ds.env_values}
        # 5분 평균 계산을 위한 과거 기록 저장용
        self.history = {key: [] for key in self.env_values}

    # env_values를 JSON 스타일로 콘솔에 출력
    def print_env_values(self):
        print('{')
        for i, (key, value) in enumerate(self.env_values.items()):
            comma = ',' if i < len(self.env_values) - 1 else ''
            print(f"  '{key}': {value:.4f}{comma}")
        print('}')

    # 센서 데이터를 5초마다 읽고 출력하는 메서드
    def get_sensor_data(self):
        count = 0  # 반복 횟수 카운트
        try:
            while True:
                # 센서에서 데이터 수신
                current = self.ds.get_env()

                # 현재 값을 env_values에 저장하고, history에도 추가
                for key in self.env_values:
                    self.env_values[key] = current[key]
                    self.history[key].append(current[key])
                    # 가장 오래된 기록 제거 (최대 60개만 유지 = 5분치)
                    if len(self.history[key]) > 60:
                        self.history[key].pop(0)

                # 현재 값 출력 (JSON 형식)
                self.print_env_values()

                count += 1
                # 60번마다 (5분마다) 평균 출력
                if count % 60 == 0:
                    print('\n[5분 평균]')
                    for key in self.env_values:
                        avg = sum(self.history[key]) / len(self.history[key])
                        print(f'{key}: {avg:.2f}')
                    print()

                # 5초 대기
                time.sleep(5)

        # 사용자가 Ctrl + C를 누르면 실행 종료
        except KeyboardInterrupt:
            print('System stopped...')


# 문제 3에서 제작한 DummySensor 클래스를 ds라는 이름으로 인스턴스화
ds = DummySensor()

# MissionComputer 클래스를 RunComputer라는 이름으로 인스턴스화
RunComputer = MissionComputer(ds)

# RunComputer 인스턴스의 get_sensor_data() 메소드를 호출하여 동작 시작
RunComputer.get_sensor_data()
