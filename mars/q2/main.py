def read_csv(filename):
    """
    CSV 파일을 읽어 내용을 문자열로 반환하는 함수.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()  # 파일의 모든 내용을 읽어옴
            return content
    except FileNotFoundError:
        print(f'파일 "{filename}"을 찾을 수 없습니다.')
        return None
    except Exception as e:
        print(f'파일을 읽는 중 오류 발생: {e}')
        return None
    
def parse_csv(content):
    """
    CSV 내용을 파싱하여 헤더와 데이터를 리스트로 반환하는 함수.
    """
    try:
        lines = content.strip().split('\n')  # 내용을 줄 단위로 분리
        header = lines[0].strip().split(',')  # 첫 줄을 헤더로 사용
        data_list = [line.strip().split(',') for line in lines[1:]]  # 나머지 줄을 데이터로 사용
        return header, data_list
    except Exception as e:
        print(f'CSV 파싱 중 오류 발생: {e}')
        return [], []   

def sort_by_index(header, items, key):
    """
    인화성 지수를 기준으로 내림차순 정렬
    """
    try:
        index = header.index(key)  # 인화성 지수의 열 인덱스 찾기
        items.sort(key=lambda x: float(x[index]) if x[index].replace('.', '', 1).isdigit() else 0, reverse=True)
    except ValueError:
        print(f'헤더 "{key}"가 존재하지 않습니다.')
    except Exception as e:
        print(f'정렬 중 오류 발생: {e}')

def filter_by_index(header, items, key, threshold=0.7):
    """
    지정된 값(threshold) 이상인 항목 필터링
    """
    try:
        index = header.index(key)
        return [item for item in items if float(item[index]) >= threshold]
    except ValueError:
        print(f'헤더 "{key}"가 없습니다.')
        return []
    except Exception as e:
        print(f'필터링 중 오류 발생: {e}')
        return []

def write_csv(header, items, filename):
    """
    리스트 데이터를 CSV 파일로 저장
    """
    try:
        with open(filename, 'w') as file:
            file.write(','.join(header) + '\n')  # 헤더 작성
            for item in items:
                file.write(','.join(item) + '\n')
    except Exception as e:
        print(f'CSV 파일 저장 오류: {e}')

def write_bin(header, items, filename):
    """
    정렬된 리스트를 이진 파일로 저장
    """
    try:
        with open(filename, 'wb') as file:
            file.write(','.join(header).encode() + b'\n')
            for item in items:
                file.write(','.join(item).encode() + b'\n')
    except Exception as e:
        print(f'이진 파일 저장 오류: {e}')

def read_bin(filename):
    """
    이진 파일을 읽어 리스트로 반환
    """
    try:
        with open(filename, 'rb') as file:
            return [line.decode().strip().split(',') for line in file.readlines()]            
    except Exception as e:
        print(f'이진 파일 읽기 오류: {e}')
        return []

def main():
    filename = 'Mars_Base_Inventory_List.csv'
    content = read_csv(filename)  # 파일을 읽음
    if content is None: # 파일을 읽지 못한 경우
        print("파일을 읽을 수 없으므로 프로그램을 종료합니다.") 
        return
    
    print("\n {filename} 내용:")
    print(content)
    
    header, items = parse_csv(content)  # 내용을 파싱하여 헤더와 데이터를 얻음
    
    print('\n리스트로 변환된 내용:')
    for item in items:
        print(item)

    
    print('\n리스트로 변환된 내용:')
    for item in items:
        print(item)
    
    fire_index = 'Flammability'  
    sort_by_index(header, items, fire_index)
    print('\n인화성 지수 기준 정렬된 목록:')
    for item in items:
        print(item)
    
    high_fire_items = filter_by_index(header, items, fire_index, 0.7)
    print('\n인화성 지수 0.7 이상:')
    for item in high_fire_items:
        print(item)
    
    danger_filename = 'Mars_Base_Inventory_danger.csv'
    write_csv(header, high_fire_items, danger_filename)
    print(f'\n인화성 높은 목록 "{danger_filename}" 저장 완료.')
    
    bin_filename = 'Mars_Base_Inventory_List.bin'
    write_bin(header, items, bin_filename)
    print(f'정렬된 목록 "{bin_filename}" 이진 파일 저장 완료.')
    
    binary_contents = read_bin(bin_filename)
    print('\n이진 파일에서 읽어온 내용:')
    for item in binary_contents:
        print(item)
    
    print("\n텍스트 파일 vs 이진 파일:")
    print("텍스트 파일은 사람이 읽기 쉽지만 크기가 크고 속도가 느릴 수 있음.")
    print("이진 파일은 저장 공간을 절약하고 속도가 빠르지만 사람이 직접 읽기 어려움.")

if __name__ == '__main__':
    main()
