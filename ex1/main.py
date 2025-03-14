print('Hello Mars')

# 로그 파일을 읽어들이는 함수
def read_log(file_name):
    """
    주어진 파일 이름의 로그 파일을 읽고 내용을 반환합니다.
    
    :param file_name: 로그 파일 이름
    :return: 로그 데이터 리스트
    """
    try:
        # 로그 파일을 열고 내용 읽기
        with open(file_name, 'r', encoding='utf-8') as file:
            log_data = file.readlines()
        return log_data
    except FileNotFoundError:
        # 파일을 찾을 수 없을 때 처리
        print(f'파일 "{file_name}"을 찾을 수 없습니다.')
        return []
    except Exception as e:
        # 그 외의 예외 처리
        print(f'오류 발생: {e}')
        return []

# 로그 데이터를 화면에 출력하는 함수
def print_log(log_data):
    """
    로그 데이터를 화면에 출력합니다.
    
    :param log_data: 로그 데이터 리스트
    """
    if log_data:
        for line in log_data:
            print(line.strip())

# 로그 분석 함수
def analyze_log(log_data):
    """
    로그 데이터에서 'Oxygen tank explosion' 이벤트를 분석합니다.
    
    :param log_data: 로그 데이터 리스트
    :return: 폭발 전, 폭발 로그, 폭발 후 로그 리스트
    """
    explosion_indices = [i for i, line in enumerate(log_data) if 'Oxygen tank explosion' in line]
    
    if explosion_indices:
        explosion_index = explosion_indices[-1]  # 마지막 폭발 인덱스
        before_explosion = log_data[max(0, explosion_index - 5):explosion_index]
        after_explosion = log_data[explosion_index + 1:explosion_index + 6]
        return before_explosion, log_data[explosion_index], after_explosion
    return None, None, None

# 사고 분석 후 보고서 생성 함수
def generate_report(before, explosion, after):
    """
    사고 분석 결과를 Markdown 형식으로 보고서를 작성합니다.
    
    :param before: 폭발 전 로그 리스트
    :param explosion: 폭발 로그
    :param after: 폭발 후 로그 리스트
    """
    accident_time = explosion.split(' ')[0]  # 사고 발생 시간 추출
    report = f"""
    # 사고 분석 보고서

    ## 사고 개요
    - 사고 발생 시간: {accident_time}
    - 사고 위치: 로켓 시스템 (Oxygen Tank)

    ## 폭발 전 로그
    ```txt
    """
    for line in before:
        report += f'{line.strip()}\n'

    report += """
    ```

    ## 폭발 로그
    ```txt
    """
    report += f'{explosion.strip()}\n'
    report += """
    ```

    ## 폭발 후 로그
    ```txt
    """
    for line in after:
        report += f'{line.strip()}\n'

    report += """
    ```

    ## 사고 원인 분석
    - 로그에 따르면, 'Oxygen tank explosion'은 {accident_time}에 발생한 것으로 보이며, 그 직전까지 정상적인 운영이 이루어졌습니다.
    - 사고의 근본 원인으로는 산소 탱크의 불안정성 문제가 발생했음을 알 수 있습니다.
    """
    
    # 보고서 저장
    with open('log_analysis.md', 'w', encoding='utf-8') as file:
        file.write(report)

    print('보고서가 "log_analysis.md"로 저장되었습니다.')

# 로그를 역순으로 정렬하고 문제 로그를 파일로 저장하는 함수
def reverse_and_find_problems(log_data):
    """
    로그 데이터를 역순으로 정렬하고 문제 로그를 파일로 저장합니다.
    
    :param log_data: 로그 데이터 리스트
    """
    # 로그를 시간 역순으로 정렬
    log_data.reverse()

    # 문제 로그만 따로 파일로 저장
    problem_logs = [line.strip() for line in log_data if 'Oxygen tank explosion' in line]
    
    if problem_logs:
        with open('problem_logs.txt', 'w', encoding='utf-8') as file:
            for line in problem_logs:
                file.write(line + '\n')

    # 시간 역순으로 출력
    for line in log_data:
        print(line.strip())

# 최종 main 함수
def main():
    log_file = 'mission_computer_main.log'
    log_data = read_log(log_file)
    
    # 로그 데이터를 읽을 수 없는 경우 종료
    if not log_data:
        return

    # 로그 출력 (전체 로그)
    print_log(log_data)

    # 로그 분석 (Oxygen tank explosion 찾기)
    before, explosion, after = analyze_log(log_data)
    if before and explosion and after:
        generate_report(before, explosion, after)
    else:
        print('로그에서 "Oxygen tank explosion"을 찾을 수 없습니다.')

    # 역순 정렬 및 문제 로그 저장
    reverse_and_find_problems(log_data)

if __name__ == '__main__':
    main()
