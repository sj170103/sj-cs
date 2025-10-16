# crawling_KBS.py

import time
import sys
import csv
import getpass  # 비밀번호를 안전하게 입력받기 위해 추가
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def get_login_driver():
    """
    터미널에서 직접 아이디와 비밀번호를 입력받아 네이버 로그인을 수행하고,
    로그인된 드라이버 객체를 반환합니다.
    """
    # 1. 터미널에서 아이디와 비밀번호 직접 입력받기
    print("네이버 로그인이 필요합니다.")
    naver_id = input("아이디를 입력하세요: ")
    # getpass는 터미널에서 입력되는 내용을 숨겨줍니다.
    naver_password = getpass.getpass("비밀번호를 입력하세요 (입력 내용은 보이지 않습니다): ")

    # 아이디나 비밀번호가 입력되지 않았을 경우, 에러 메시지 출력 후 종료
    if not naver_id or not naver_password:
        print('오류: 아이디와 비밀번호를 모두 입력해야 합니다.')
        sys.exit()

    # 2. 크롬 브라우저 실행
    driver = webdriver.Chrome()

    # 3. 네이버 로그인 페이지로 이동
    driver.get('https://nid.naver.com/nidlogin.login')
    time.sleep(1)

    # 4. 아이디와 비밀번호 입력 (봇 탐지 우회 방식)
    driver.execute_script(f"document.getElementById('id').value = '{naver_id}'")
    time.sleep(1)
    driver.execute_script(f"document.getElementById('pw').value = '{naver_password}'")
    time.sleep(1)

    # 5. 로그인 버튼 클릭
    driver.find_element(By.ID, 'log.login').click()
    
    # 2단계 인증 등 수동 처리를 위한 대기 시간
    time.sleep(5)
    
    return driver

def get_user_nickname(driver):
    """
    로그인된 드라이버를 사용하여 네이버 메인의 닉네임을 가져옵니다.
    """
    try:
        driver.get('https://www.naver.com')
        time.sleep(2)
        account_div = driver.find_element(By.ID, 'account')
        nickname_element = account_div.find_element(By.CSS_SELECTOR, '[class^="MyView-module__nickname"]')
        return nickname_element.text
    except NoSuchElementException:
        return '닉네임을 찾을 수 없습니다 (로그인 실패 가능성 확인)'
    except Exception as e:
        return f'닉네임 추출 중 오류 발생: {e}'

def get_unread_mail_titles(driver):
    """
    로그인된 드라이버를 사용하여 읽지 않은 메일 제목들을 가져옵니다.
    """
    mail_titles = []
    try:
        # 요청하신 대로 정확한 메일함 경로로 수정
        driver.get('https://mail.naver.com/v2/folders/-1')
        time.sleep(3) # 메일 목록 로딩 대기
        
        # 제공해주신 HTML 구조에 맞춰 더 정확한 선택자로 수정
        # div.mail_title 내부의 span.text 요소를 찾습니다.
        title_elements = driver.find_elements(By.CSS_SELECTOR, 'div.mail_title span.text')
        for element in title_elements:
            mail_titles.append(element.text)
        return mail_titles
    except Exception as e:
        print(f'메일 제목 추출 중 오류 발생: {e}')
        return []

def save_to_csv(nickname, mail_list):
    """
    크롤링한 닉네임과 메일 제목 리스트를 CSV 파일로 저장합니다.
    """
    filename = 'naver_crawl_result.csv'
    try:
        # 한글 깨짐 방지를 위해 encoding='utf-8-sig' 옵션 사용
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(['구분', '내용'])
            writer.writerow(['닉네임', nickname])
            for title in mail_list:
                writer.writerow(['메일제목', title])
        
        print(f"✅ 성공: 크롤링 결과가 '{filename}' 파일로 저장되었습니다.")

    except Exception as e:
        print(f"❌ 오류: CSV 파일 저장에 실패했습니다. {e}")

if __name__ == '__main__':
    logged_in_driver = get_login_driver()
    user_nickname = get_user_nickname(logged_in_driver)
    unread_mails = get_unread_mail_titles(logged_in_driver)
    
    logged_in_driver.quit()

    # --- 화면 출력 부분 ---
    result_list = [user_nickname]
    print('\n--- 로그인 후 확인된 닉네임 ---')
    print(result_list)
    
    print('\n--- 읽지 않은 메일 제목 목록 (보너스) ---')
    if unread_mails:
        print(unread_mails)
    else:
        print('읽지 않은 메일이 없거나, 제목을 가져올 수 없습니다.')

    # --- 파일 저장 함수 호출 ---
    print("\n--- CSV 파일 저장 시작 ---")
    save_to_csv(user_nickname, unread_mails)

