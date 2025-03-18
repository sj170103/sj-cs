print('Hello Mars')

def read_log(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.readlines()
    except FileNotFoundError:
        print('Error: 로그 파일을 찾을 수 없습니다.')
        return []
    except Exception as e:
        print(f'오류 발생: {e}')
        return []

def display_logs(logs):
    for log in logs:
        print(log.strip())

def analyze_logs():
    file_name = 'mission_computer_main.log'
    logs = read_log(file_name)
    
    if logs:
        print('Mission Log Data:\n')
        display_logs(logs)

def display_logs_reversed(logs):
    for log in reversed(logs):
        print(log.strip())

def extract_critical_logs(logs):
    return [log for log in logs if 'Oxygen tank' in log or 'explosion' in log or 'powered down' in log]

def save_logs(logs, output_file):
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.writelines("\n".join(logs))
        print(f'문제가 되는 부분은 {output_file}에 따로 저장되었습니다.')
    except Exception as e:
        print(f'오류 발생: {e}')

def process_bonus():
    file_name = 'mission_computer_main.log'
    logs = read_log(file_name)
    
    if logs:
        print('\nMission Log Data (Reversed):\n')
        display_logs_reversed(logs)
        
        print('\nExtracting critical events...')
        critical_logs = extract_critical_logs(logs)
        save_logs(critical_logs, 'critical_events.log')

if __name__ == '__main__':
    analyze_logs()
    process_bonus()
