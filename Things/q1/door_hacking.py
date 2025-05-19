import zipfile
import time


def unlock_zip():
    """암호가 걸린 ZIP 파일을 브루트포스로 해제하는 함수"""
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    total_attempts = 0
    start_time = time.time()

    try:
        zip_file = zipfile.ZipFile('emergency_storage_key.zip')
    except FileNotFoundError:
        print('zip 파일이 존재하지 않습니다.')
        return

    print('비밀번호 해제 시도 시작...')
    print(f'시작 시간: {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))}')

    for c1 in chars:
        for c2 in chars:
            for c3 in chars:
                for c4 in chars:
                    for c5 in chars:
                        for c6 in chars:
                            password = c1 + c2 + c3 + c4 + c5 + c6
                            total_attempts += 1

                            try:
                                zip_file.extractall(pwd=bytes(password, 'utf-8'))

                                elapsed_time = time.time() - start_time
                                print(f'비밀번호를 찾았습니다: {password}')
                                print(f'총 시도 횟수: {total_attempts}')
                                print(f'소요 시간: {elapsed_time:.2f}초')

                                with open('password.txt', 'w') as f:
                                    f.write(password)

                                return
                            except:
                                if total_attempts % 100000 == 0:
                                    elapsed = time.time() - start_time
                                    print(f'{total_attempts}회 시도됨... 경과 시간: {elapsed:.2f}초')

    print('비밀번호를 찾지 못했습니다.')


if __name__ == '__main__':
    unlock_zip()
