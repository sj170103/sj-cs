import socket
import threading
from server_chat import PORT


def recv_loop(sock: socket.socket) -> None:
    try:
        while True:
            data = sock.recv(1024)
            if not data:
                print('서버 연결이 종료되었습니다.')
                break
            print(data.decode('utf-8').rstrip())
    except Exception:
        pass
    finally:
        try:
            sock.close()
        except Exception:
            pass


def run_client(host: str = '127.0.0.1', port=PORT ) -> None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print(f'서버에 접속했습니다: {host}:{port}')

    nickname = input('사용자명을 입력하세요: ').strip()
    if not nickname:
        nickname = 'guest'
    sock.sendall((nickname + '\n').encode('utf-8'))

    t = threading.Thread(target=recv_loop, args=(sock,), daemon=True)
    t.start()

    try:
        while True:
            msg = input()
            sock.sendall((msg + '\n').encode('utf-8'))
            if msg.strip() == '/종료':
                break
    finally:
        try:
            sock.close()
        except Exception:
            pass
        print('클라이언트를 종료합니다.')


if __name__ == '__main__':
    run_client()
