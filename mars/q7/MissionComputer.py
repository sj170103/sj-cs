import time  # 시간 측정과 지연을 위해 time 모듈은 사용 가능 (문제에서 허용됨)

# 센서 역할을 하는 더미 클래스 정의
class DummySensor:
    def __init__(self):
        self.count = 0  # 반복마다 값이 달라지도록 하는 변수

    # 센서 값들을 사전 형태로 반환
    def get_values(self):
        self.count += 1  # 호출될 때마다 count 증가
        return {
            'mars_base_internal_temperature': 20 + (self.count % 3),  # 20~22
            'mars_base_external_temperature': -70 + (self.count % 5),  # -70~-66
            'mars_base_internal_humidity': 40 + (self.count % 4),  # 40~43
            'mars_base_external_illuminance': 3000 + (self.count % 100),  # 3000~3099
            'mars_base_internal_co2': 500 + (self.count % 20),  # 500~519
            'mars_base_internal_oxygen': 21 + ((-1) ** self.count) * 0.2  # 20.8 ↔ 21.2 반복
        }

# 미션 컴퓨터 클래스
class MissionComputer:
    def __init__(self):
        self.ds = DummySensor()  # 센서 인스턴스 생성
        self.env_values = {}  # 현재 센서 값을 저장할 딕셔너리
        self.history = {}  # 5분 평균을 계산하기 위해 값을 누적할 딕셔너리
        self.running = True  # 루프를 계속할지 여부를 결정하는 플래그

    # env_values 딕셔너리를 보기 좋게 문자열로 출력하는 함수 (json 없이 직접 구현)
    def format_env(self):
        result = '{\n'
        for k, v in self.env_values.items():
            result += f"  '{k}': {v:.2f},\n"  # key: value 형식으로 정리
        result += '}'
        return result

    # 센서 데이터를 주기적으로 수집하고 출력하는 함수
    def get_sensor_data(self):
        start = time.time()  # 시작 시간 저장
        loop_count = 0  # 루프 횟수 카운트 (종료 조건으로 사용)

        while self.running:
            loop_count += 1  # 루프 돌 때마다 카운트 증가

            # 센서 값을 받아서 env_values에 저장
            self.env_values = self.ds.get_values()

            # 환경 값을 문자열로 출력
            print(self.format_env())

            # 평균 계산을 위해 history에 센서 값들을 누적
            for k in self.env_values:
                if k not in self.history:
                    self.history[k] = []  # 해당 key가 없다면 리스트 생성
                self.history[k].append(self.env_values[k])  # 값 누적

            # 5분(300초)마다 평균 출력
            if time.time() - start >= 300:
                print('=== 5분 평균 ===')
                for k, v in self.history.items():
                    avg = sum(v) / len(v)  # 평균 계산
                    print(f'{k}: {avg:.2f}')
                self.history.clear()  # 평균 출력 후 초기화
                start = time.time()  # 타이머 리셋

            # 종료 조건 (30회 반복 = 150초 후 자동 종료) ← threading 사용 못하므로 임시 방법
            if loop_count >= 30:
                self.running = False

            time.sleep(5)  # 5초 기다렸다가 다음 루프 반복

        print('System stopped...')  # 종료 메시지 출력

# 프로그램 실행 부분
if __name__ == '__main__':
    RunComputer = MissionComputer()  # 인스턴스 생성
    RunComputer.get_sensor_data()  # 센서 수집 함수 실행
