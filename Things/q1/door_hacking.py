import zipfile
import time
import io
from multiprocessing import Pool, cpu_count

CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789'
LETTERS = 'abcdefghijklmnopqrstuvwxyz'
DIGITS = '0123456789'

# zip 파일을 메모리에 한번만 로딩
with open('emergency_storage_key.zip', 'rb') as f:
    zip_bytes = f.read()

# ✅ 비밀번호를 찾으면 문자열을 리턴 (파일 저장은 하지 않음)
def try_password(pw):
    try:
        with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
            zf.extractall(pwd=bytes(pw, 'utf-8'))
            return pw  # ✅ 비밀번호를 리턴
    except:
        return None

# 중첩 루프 생성기 (itertools 없이 직접 구현)
def _nested_loop(charset, repeat):
    if repeat == 1:
        for a in charset:
            yield [a]
    elif repeat == 2:
        for a in charset:
            for b in charset:
                yield [a, b]
    elif repeat == 3:
        for a in charset:
            for b in charset:
                for c in charset:
                    yield [a, b, c]
    elif repeat == 4:
        for a in charset:
            for b in charset:
                for c in charset:
                    for d in charset:
                        yield [a, b, c, d]
    elif repeat == 5:
        for a in charset:
            for b in charset:
                for c in charset:
                    for d in charset:
                        for e in charset:
                            yield [a, b, c, d, e]
    elif repeat == 6:
        for a in charset:
            for b in charset:
                for c in charset:
                    for d in charset:
                        for e in charset:
                            for f in charset:
                                yield [a, b, c, d, e, f]

def generate_letters_digits(letter_len, digit_len, label):
    print(label)
    for a in _nested_loop(LETTERS, letter_len):
        for b in _nested_loop(DIGITS, digit_len):
            yield ''.join(a + b)

def generate_digits_letters(digit_len, letter_len, label):
    print(label)
    for a in _nested_loop(DIGITS, digit_len):
        for b in _nested_loop(LETTERS, letter_len):
            yield ''.join(a + b)

def generate_remaining_combinations(tried):
    print('[7단계] 나머지 전체 조합')
    for a in _nested_loop(CHARS, 6):
        pw = ''.join(a)
        if pw not in tried:
            yield pw

# ✅ 비밀번호 저장은 메인 프로세스에서만 수행
def save_password(pw):
    with open('password.txt', 'w') as f:
        f.write(pw)
    print(f'✅ 비밀번호를 찾았습니다: {pw}')
    print('📁 password.txt에 저장 완료')

def run_strategy(generator, tried_set=None, use_parallel=True, chunk=10000, global_start=None, total_attempts=None):
    if use_parallel:
        with Pool(cpu_count()) as pool:
            for result in pool.imap_unordered(try_password, generator, chunksize=chunk):
                total_attempts[0] += 1
                if total_attempts[0] % 100000 == 0:
                    print(f'{total_attempts[0]}회 시도됨... 누적 경과 시간: {time.time() - global_start:.2f}초')
                if result:  # result는 성공한 비밀번호 문자열
                    pool.terminate()
                    save_password(result)  # ✅ 여기서 저장
                    return True
    else:
        for pw in generator:
            total_attempts[0] += 1
            result = try_password(pw)
            if result:
                save_password(result)
                return True
            if tried_set is not None:
                tried_set.add(pw)
            if total_attempts[0] % 1000 == 0:
                print(f'{total_attempts[0]}회 시도됨... 누적 경과 시간: {time.time() - global_start:.2f}초')
    return False

def unlock_zip():
    print('비밀번호 해제 시작')
    global_start = time.time()
    print('시작 시간:', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(global_start)))
    tried = set()
    total_attempts = [0]

    if run_strategy(generate_letters_digits(3, 3, '[1단계] 영문3 + 숫자3'), tried, global_start=global_start, total_attempts=total_attempts): return
    if run_strategy(generate_letters_digits(4, 2, '[2단계] 영문4 + 숫자2'), tried, global_start=global_start, total_attempts=total_attempts): return
    if run_strategy(generate_letters_digits(5, 1, '[3단계] 영문5 + 숫자1'), tried, global_start=global_start, total_attempts=total_attempts): return

    if run_strategy(generate_digits_letters(3, 3, '[4단계] 숫자3 + 영문3'), tried, global_start=global_start, total_attempts=total_attempts): return
    if run_strategy(generate_digits_letters(4, 2, '[5단계] 숫자4 + 영문2'), tried, global_start=global_start, total_attempts=total_attempts): return
    if run_strategy(generate_digits_letters(5, 1, '[6단계] 숫자5 + 영문1'), tried, global_start=global_start, total_attempts=total_attempts): return

    if run_strategy(generate_remaining_combinations(tried), global_start=global_start, total_attempts=total_attempts): return

    print('❌ 비밀번호를 찾지 못했습니다.')

if __name__ == '__main__':
    unlock_zip()
