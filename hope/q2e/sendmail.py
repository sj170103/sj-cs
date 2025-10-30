# sendmail.py — 과제2(HTML + CSV). 개별 발송 선택, 그룹 Bcc 호출 주석 처리.
import csv
import smtplib
import html
from getpass import getpass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import parseaddr

csv_path = 'mail_target_list.csv'

def load_recipients(csv_path):
    rows = []
    with open(csv_path, 'r', encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        for r in reader:
            name = (r.get('이름') or '').strip()
            email = (r.get('이메일') or '').strip()
            if parseaddr(email)[1]:
                rows.append({'name': name, 'email': email})
    return rows


def build_message(sender_email, to_addr, subject, name):
    msg = MIMEMultipart('alternative')
    msg['From'] = sender_email
    msg['To'] = to_addr
    msg['Subject'] = subject

    name_safe = (name or '').strip()
    text = f'{name_safe}님 안녕하세요.' if name_safe else '안녕하세요.'
    html_body = (
        f'<!doctype html><html><body>{html.escape(name_safe)}님 안녕하세요.</body></html>'
        if name_safe else '<!doctype html><html><body>안녕하세요.</body></html>'
    )

    msg.attach(MIMEText(text, 'plain', _charset='utf-8'))
    msg.attach(MIMEText(html_body, 'html', _charset='utf-8'))
    return msg


def send_individual(server, sender_email, recipients):
    ok, fail = 0, 0
    subject = 'hello'
    for r in recipients:
        name = r.get('name', '')
        to_addr = r['email']
        msg = build_message(sender_email, to_addr, subject, name)
        try:
            server.sendmail(sender_email, [to_addr], msg.as_string())
            ok += 1
        except Exception as e:
            print(f'실패: {to_addr} ({e})')
            fail += 1
    print(f'완료(개별): 성공 {ok} / 실패 {fail} / 총 {len(recipients)}')


 # 참고용(시도 결과, 개인정보/전달율 이슈로 개별 발송 선택)
# def send_group_bcc(server, sender_email, recipients):
#     emails = [r['email'] for r in recipients]
#     subject = 'hello'
#     msg = MIMEMultipart('alternative')
#     msg['From'] = sender_email
#     msg['To'] = 'undisclosed-recipients:;'
#     msg['Subject'] = subject
#     text = 'hello'
#     html = '<!doctype html><html><body>hello</body></html>'
#     msg.attach(MIMEText(text, 'plain', _charset='utf-8'))
#     msg.attach(MIMEText(html, 'html', _charset='utf-8'))
#     server.sendmail(sender_email, emails, msg.as_string())


def connect_smtp(provider, sender, password):
    if provider == 'naver':
        # 1순위: STARTTLS(587) → 실패 시 SSL(465) 폴백
        try:
            s = smtplib.SMTP('smtp.naver.com', 587, timeout=30)
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(sender, password)
            return s
        except Exception:
            try:
                s.quit()
            except Exception:
                pass
            s = smtplib.SMTP_SSL('smtp.naver.com', 465, timeout=30)
            s.login(sender, password)
            return s
    else:
        # gmail 기본: SSL(465)
        s = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=30)
        s.login(sender, password)
        return s


if __name__ == '__main__':
    provider = input('SMTP 제공자 [gmail/naver] (기본: gmail): ').strip().lower() or 'gmail'
    sender = input('보내는 사람 이메일(로그인 계정과 동일): ').strip()
    password = getpass('SMTP 비밀번호(또는 앱 비밀번호): ').strip()
    

    recipients = load_recipients(csv_path)
    if not recipients:
        print('CSV에서 유효한 수신자가 없습니다.')
        raise SystemExit(1)

    try:
        server = connect_smtp(provider, sender, password)
        try:
            # 선택: 개별 발송(활성)
            send_individual(server, sender, recipients)

            # 비활성: 그룹 Bcc(시도 흔적만 남김)
            # send_group_bcc(server, sender, recipients)
        finally:
            try:
                server.quit()
            except Exception:
                pass
    except smtplib.SMTPAuthenticationError:
        print(' SMTP 인증 실패: 계정/비밀번호 확인')
    except Exception as e:
        print(f' SMTP 오류: {e}')
