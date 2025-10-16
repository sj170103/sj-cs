# sendmail.py (사용자 입력 및 첨부파일 기능)

import smtplib
import sys
from getpass import getpass 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_email_with_attachment(sender_email, app_password, receiver_email, subject, body, attachment_path=None):
    '''
    텍스트 이메일을 발송하며, 선택적으로 파일을 첨부합니다.

    Args:
        sender_email (str): 보내는 사람의 Gmail 주소
        app_password (str): 보내는 사람의 Gmail 앱 비밀번호 (16자리)
        receiver_email (str): 받는 사람의 이메일 주소
        subject (str): 이메일 제목
        body (str): 이메일 본문 내용
        attachment_path (str, optional): 첨부할 파일의 경로. Defaults to None.
    '''
    smtp_server = 'smtp.gmail.com'
    smtp_port = 465

    # 메시지 컨테이너를 MIMEMultipart로 생성
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # 이메일 본문(텍스트 부분) 추가
    msg.attach(MIMEText(body, 'plain'))

    # 첨부 파일 경로가 있고, 비어있지 않다면 파일 부분 추가
    if attachment_path and attachment_path.strip():
        try:
            with open(attachment_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            # Base64로 인코딩
            encoders.encode_base64(part)
            
            # 파일 이름을 Content-Disposition 헤더에 추가
            filename = attachment_path.split('/')[-1].split('\\')[-1]
            part.add_header(
                'Content-Disposition',
                f'attachment; filename="{filename}"'
            )
            
            # 메시지에 파일 부분 첨부
            msg.attach(part)
            print(f"✅ '{filename}' 파일이 첨부되었습니다.")
        except FileNotFoundError:
            print(f"❌ 오류: 첨부 파일을 찾을 수 없습니다. 경로: {attachment_path}")
            return
        except Exception as e:
            print(f"❌ 오류: 파일을 첨부하는 중 문제가 발생했습니다: {e}")
            return

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
            print(f"\n🚀 성공적으로 메일을 보냈습니다. (첨부: {'있음' if attachment_path and attachment_path.strip() else '없음'})")

    except smtplib.SMTPAuthenticationError:
        print('❌ 오류: SMTP 인증에 실패했습니다. 이메일 주소와 앱 비밀번호를 확인하세요.')
    except Exception as e:
        print(f'❌ 메일 발송 중 오류가 발생했습니다: {e}')


# --- 프로그램 실행 부분 ---
if __name__ == '__main__':
    print('=== 📧 Gmail 메일 발송 프로그램을 시작합니다 ===')

    # 1. 사용자로부터 이메일 정보 입력받기
    my_email = input('보내는 사람 Gmail 주소: ').strip()
    my_app_password = getpass('Gmail 앱 비밀번호(16자리): ').strip()
    recipient_email = input('받는 사람 이메일 주소: ').strip()
    
    # 2. 메일 제목 및 본문을 기본값으로 설정
    subject = '자동 발송된 테스트 메일입니다.'
    body = '이 메일은 Python 스크립트를 통해 자동으로 생성 및 발송되었습니다.'
    print(f"✅ 제목과 본문이 기본값으로 설정되었습니다.")
    
    # 3. 첨부 파일 경로 입력받기 (선택 사항)
    attachment_path = input('첨부할 파일의 전체 경로 (없으면 Enter): ').strip()

    # 4. 필수 정보가 입력되었는지 확인 후 메일 발송
    if not all([my_email, my_app_password, recipient_email]):
        print('\n❌ 필수 정보(보내는 사람, 비밀번호, 받는 사람)가 누락되어 메일을 발송할 수 없습니다.')
    else:
        send_email_with_attachment(
            my_email,
            my_app_password,
            recipient_email,
            subject,
            body,
            attachment_path
        )

