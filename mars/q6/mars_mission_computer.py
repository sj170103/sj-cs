import random
import time

# DummySensor 클래스 정의
# 화성 기지의 더미 센서를 시뮬레이션하는 역할
class DummySensor:
    def __init__(self):
        # 센서 환경값들을 저장할 딕셔너리 초기화
        self.env_values = {
            'mars_base_internal_temperature': 0.0,      # 내부 온도 (18~30도)
            'mars_base_external_temperature': 0.0,      # 외부 온도 (0~21도)
            'mars_base_internal_humidity': 0.0,         # 내부 습도 (50~60%)
            'mars_base_external_illuminance': 0.0,      # 외부 광량 (500~715 W/m²)
            'mars_base_internal_co2': 0.0,              # 내부 이산화탄소 농도 (0.02~0.1%)
            'mars_base_internal_oxygen': 0.0            # 내부 산소 농도 (4~7%)
        }

    # 환경값을 무작위로 설정하는 메서드
    def set_env(self):
        self.env_values['mars_base_internal_temperature'] = random.uniform(18, 30)
        self.env_values['mars_base_external_temperature'] = random.uniform(0, 21)
        self.env_values['mars_base_internal_humidity'] = random.uniform(50, 60)
        self.env_values['mars_base_external_illuminance'] = random.uniform(500, 715)
        self.env_values['mars_base_internal_co2'] = random.uniform(0.02, 0.1)
        self.env_values['mars_base_internal_oxygen'] = random.uniform(4, 7)

    # 환경값 반환 및 로그 파일 작성 메서드
    def get_env(self):
        # 로그 문자열 생성 (날짜 및 각 항목 소수점 포맷 적용)
        log_line = '{time}, {internal_temp:.2f}, {external_temp:.2f}, {humidity:.2f}, {illuminance:.2f}, {co2:.4f}, {oxygen:.2f}\n'.format(
            time=time.strftime('%Y-%m-%d %H:%M:%S'),
            internal_temp=self.env_values['mars_base_internal_temperature'],
            external_temp=self.env_values['mars_base_external_temperature'],
            humidity=self.env_values['mars_base_internal_humidity'],
            illuminance=self.env_values['mars_base_external_illuminance'],
            co2=self.env_values['mars_base_internal_co2'],
            oxygen=self.env_values['mars_base_internal_oxygen']
        )

        # 로그 파일에 내용 추가 (덮어쓰기 아님)
        with open('sensor_log.txt', 'a') as file:
            file.write(log_line)

        # 현재 환경값 반환
        return self.env_values


# DummySensor 인스턴스 생성
ds = DummySensor()

# 랜덤 환경값 생성
ds.set_env()

# 센서값 조회 및 로그 작성
env_data = ds.get_env()

# 콘솔에 현재 센서값 출력
print('현재 센서 데이터:')
for key, value in env_data.items():
    print(f'{key}: {value:.2f}')
