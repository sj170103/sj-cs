import socket
import threading
from typing import Dict, Tuple, Optional

# -------------------------
# 공용 상수
# -------------------------
HOST: str = '0.0.0.0'
PORT: int = 5000
ADMIN_SHUTDOWN_CMD: str = '/shutdown'


class ChatServer:
    def __init__(self, host: str = HOST, port: int = PORT) -> None:
        self.host = host
        self.port = port
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients_lock = threading.Lock()
        # sock -> nickname
        self.clients: Dict[socket.socket, str] = {}

    def start(self) -> None:
        """서버 시작: 관리 입력 스레드 기동 후 클라이언트 접속을 무한히 수락."""
        self.server_sock.bind((self.host, self.port))
        self.server_sock.listen()
        print(f'서버가 {self.host}:{self.port} 에서 대기 중입니다.')
        print(f'서버 종료시 /shutdown 입력')

        # -------------------------
        # 관리자 종료 명령(/shutdown) 입력 스레드
        # -------------------------
        threading.Thread(target=self._admin_loop, daemon=True).start()

        try:
            while True:
                client_sock, client_addr = self.server_sock.accept()
                print(f'클라이언트 접속: {client_addr}')
                threading.Thread(
                    target=self.handle_client,
                    args=(client_sock, client_addr),
                    daemon=True
                ).start()
        except OSError:
            # server_sock이 닫히면 accept에서 OSError 발생 → 정상 종료 경로
            pass
        finally:
            try:
                self.server_sock.close()
            except Exception:
                pass
            print('서버를 종료합니다.')

    def handle_client(self, client_sock: socket.socket, client_addr: Tuple[str, int]) -> None:
        """각 클라이언트를 담당하는 스레드."""
        try:
            nickname = self._recv_line(client_sock)
            if not nickname:
                client_sock.close()
                return

            with self.clients_lock:
                self.clients[client_sock] = nickname

            # 입장 알림
            self.broadcast(f'{nickname}님이 입장하셨습니다.', sender=None)

            while True:
                msg = self._recv_line(client_sock)
                if not msg:
                    break
                if msg.strip() == '/종료':
                    break

                # -------------------------
                # 보너스 기능: 귓속말
                # /w 닉네임 메시지 → 해당 닉네임에게만 전달
                # -------------------------
                if msg.startswith('/w '):
                    parts = msg.split(' ', 2)
                    if len(parts) < 3:
                        client_sock.sendall('사용법: /w 닉네임 메시지\n'.encode('utf-8'))
                    else:
                        _, target_name, whisper_msg = parts
                        self.whisper(client_sock, target_name, whisper_msg)
                else:
                    # 기본 기능: 전체 브로드캐스트
                    self.broadcast(f'{nickname}> {msg}', sender=client_sock)
        except Exception as exc:
            print(f'에러({client_addr}): {exc}')
        finally:
            self._disconnect(client_sock)

    def broadcast(self, message: str, sender: Optional[socket.socket]) -> None:
        """전체 클라이언트에게 메시지 전송."""
        data = (message + '\n').encode('utf-8')
        with self.clients_lock:
            dead: list[socket.socket] = []
            for sock in self.clients.keys():
                try:
                    sock.sendall(data)
                except Exception:
                    dead.append(sock)
            for sock in dead:
                self._disconnect(sock)

    # -------------------------
    # 보너스 기능: 귓속말 함수
    # -------------------------
    def whisper(self, sender_sock: socket.socket, target_name: str, message: str) -> None:
        """귓속말: 특정 닉네임에게만 메시지 전송."""
        sender_name = self.clients.get(sender_sock, 'unknown')
        target_sock = None
        with self.clients_lock:
            for sock, name in self.clients.items():
                if name == target_name:
                    target_sock = sock
                    break

        if target_sock:
            text = f'(귓속말) {sender_name}> {message}\n'
            try:
                target_sock.sendall(text.encode('utf-8'))
                sender_sock.sendall(text.encode('utf-8'))
            except Exception:
                pass
        else:
            try:
                sender_sock.sendall(f'해당 사용자를 찾을 수 없습니다: {target_name}\n'.encode('utf-8'))
            except Exception:
                pass

    def _disconnect(self, client_sock: socket.socket) -> None:
        """클라이언트 연결 종료 처리."""
        with self.clients_lock:
            nickname = self.clients.pop(client_sock, None)
        try:
            client_sock.close()
        except Exception:
            pass
        if nickname:
            self.broadcast(f'{nickname}님이 퇴장하셨습니다.', sender=None)

    @staticmethod
    def _recv_line(sock: socket.socket) -> Optional[str]:
        """개행까지 읽어서 문자열 반환. 연결 끊기면 None."""
        chunks: list[bytes] = []
        while True:
            data = sock.recv(1024)
            if not data:
                return None
            chunks.append(data)
            if b'\n' in data:
                break
        line = b''.join(chunks).split(b'\n', 1)[0]
        return line.decode('utf-8').rstrip('\r')

    # 종료 명령 처리
    def _admin_loop(self) -> None:
        """서버 콘솔에서 /shutdown 명령을 받는 루프."""
        while True:
            try:
                cmd = input()
            except EOFError:
                break

            if cmd.strip() == ADMIN_SHUTDOWN_CMD:
                print('관리자 명령으로 서버를 종료합니다.')
                self._shutdown()
                break
            elif cmd.strip():
                print(f'알 수 없는 명령입니다: {cmd.strip()}')

    def _shutdown(self) -> None:
        """공지 → 클라이언트 소켓 정리 → 서버 소켓 닫기."""
        try:
            self.broadcast('서버가 곧 종료됩니다.', sender=None)
        except Exception:
            pass

        with self.clients_lock:
            sockets = list(self.clients.keys())
        for sock in sockets:
            try:
                sock.shutdown(socket.SHUT_RDWR)
            except Exception:
                pass
            try:
                sock.close()
            except Exception:
                pass

        try:
            self.server_sock.close()
        except Exception:
            pass


def main() -> None:
    server = ChatServer(host=HOST, port=PORT)
    server.start()


if __name__ == '__main__':
    main()
