def caesar_cipher_decode(target_text, shift):
    decoded = ''
    for char in target_text:
        if 'a' <= char <= 'z':
            decoded += chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
        elif 'A' <= char <= 'Z':
            decoded += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
        else:
            decoded += char
    return decoded


def main():
    try:
        with open('password.txt', 'r', encoding='utf-8') as file:
            encrypted_text = file.read().strip()
    except FileNotFoundError:
        print('password.txt 파일이 존재하지 않습니다.')
        return
    except Exception as e:
        print(f'파일을 읽는 중 오류 발생: {e}')
        return

    print('[카이사르 암호 해독 시작]')
    print('-------------------------------')

    # 보너스: 평문에 포함될 수 있는 단어 사전
    dictionary = ['mars', 'emergency', 'security', 'key', 'station', 'mission']

    for shift in range(0, 26):  # ✅ shift=0 포함
        decoded_text = caesar_cipher_decode(encrypted_text, shift)
        print(f'{shift:2d} ▶ {decoded_text}')

        # 자동 키워드 탐지
        lower_decoded = decoded_text.lower()
        if any(word in lower_decoded for word in dictionary):
            print(f'사전 단어 발견! 해독 키: {shift}')
            save_result(decoded_text)
            return

    print('자동 탐지 실패. 사람이 직접 해독 키를 선택해야 합니다.')

    try:
        user_shift = int(input('해독 키 입력 (0~25): '))
        if not 0 <= user_shift <= 25:
            print('유효한 숫자를 입력하세요.')
            return
        final_decoded = caesar_cipher_decode(encrypted_text, user_shift)
        save_result(final_decoded)
    except ValueError:
        print('숫자만 입력 가능합니다.')


def save_result(decoded_text):
    try:
        with open('result.txt', 'w', encoding='utf-8') as result_file:
            result_file.write(decoded_text)
        print('result.txt에 저장 완료!')
    except Exception as e:
        print(f'파일 저장 중 오류 발생: {e}')


if __name__ == '__main__':
    main()
