from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json
import os
import socket
import sys
from urllib.error import URLError
from urllib.request import urlopen

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = BASE_DIR / 'templates' / 'index.html'
DEFAULT_PORT = 8080
ALLOWED_PATHS = {'/', '/index.html'}

PRIVATE_IP_HINTS = {
    '127.': 'loopback',
    '10.': 'private-net',
    '192.168.': 'private-net',
    '172.16.': 'private-net',
    '172.17.': 'private-net',
    '172.18.': 'private-net',
    '172.19.': 'private-net',
    '172.20.': 'private-net',
    '172.21.': 'private-net',
    '172.22.': 'private-net',
    '172.23.': 'private-net',
    '172.24.': 'private-net',
    '172.25.': 'private-net',
    '172.26.': 'private-net',
    '172.27.': 'private-net',
    '172.28.': 'private-net',
    '172.29.': 'private-net',
    '172.30.': 'private-net',
    '172.31.': 'private-net',
}
PRIVATE_PREFIXES = tuple(PRIVATE_IP_HINTS.keys())
_GEO_CACHE: dict[str, str] = {}


def is_public_ip(ip_address: str) -> bool:
    return not any(ip_address.startswith(prefix) for prefix in PRIVATE_PREFIXES)


def classify_client(ip_address: str) -> str:
    for prefix, label in PRIVATE_IP_HINTS.items():
        if ip_address.startswith(prefix):
            return label
    return 'public'


def sanitize_user_agent(user_agent: str) -> str:
    collapsed = ' '.join(user_agent.split())
    return collapsed[:200] if collapsed else '-'


def geolocate_ip(ip_address: str, timeout: float = 2.5) -> str:
    if not ip_address or not is_public_ip(ip_address):
        return ''
    if ip_address in _GEO_CACHE:
        return _GEO_CACHE[ip_address]
    url = (
        f'http://ip-api.com/json/{ip_address}'
        '?fields=status,country,regionName,city,timezone,message'
    )
    try:
        with urlopen(url, timeout=timeout) as response:
            payload = json.loads(response.read().decode('utf-8'))
    except (URLError, socket.timeout, ValueError, json.JSONDecodeError):
        payload = {}
    if payload.get('status') != 'success':
        _GEO_CACHE[ip_address] = ''
        return ''
    parts = [
        payload.get('country'),
        payload.get('regionName'),
        payload.get('city'),
        payload.get('timezone'),
    ]
    label = ' / '.join(part for part in parts if part)
    _GEO_CACHE[ip_address] = label
    return label


class SpacePirateHTTPRequestHandler(BaseHTTPRequestHandler):
    server_version = 'SpacePirateHTTP/1.0'

    def do_GET(self):
        if self.path in ALLOWED_PATHS:
            self._serve_index(send_body=True)
        else:
            self._respond_not_found()

    def do_HEAD(self):
        if self.path in ALLOWED_PATHS:
            self._serve_index(send_body=False)
        else:
            self._respond_not_found()

    def _serve_index(self, send_body):
        try:
            body = TEMPLATE_PATH.read_bytes()
        except FileNotFoundError:
            self._respond_missing_template()
            return

        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        if send_body:
            self.wfile.write(body)
        self._log_access(200)

    def _respond_not_found(self):
        self.send_error(404, 'Not Found')
        self._log_access(404)

    def _respond_missing_template(self):
        message = 'index.html template is missing'
        encoded = message.encode('utf-8')
        self.send_response(500, 'Internal Server Error')
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.send_header('Content-Length', str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)
        self._log_access(500)

    def _log_access(self, status_code):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        client_ip = self.client_address[0]
        segment = classify_client(client_ip)
        user_agent = sanitize_user_agent(self.headers.get('User-Agent', ''))
        geo = geolocate_ip(client_ip)
        geo_part = f' | 위치={geo}' if geo else ''
        log_line = (
            f"[접속] 시간={timestamp} | IP={client_ip} | 구간={segment}{geo_part} | "
            f"UA={user_agent} | 상태={status_code}"
        )
        print(log_line, flush=True)

    def log_message(self, format, *args):
        return


def resolve_port():
    override = os.getenv('SERVER_PORT')
    if override:
        try:
            candidate = int(override)
        except ValueError:
            pass
        else:
            if 0 < candidate < 65536:
                return candidate
            print(
                f'Ignoring invalid SERVER_PORT value: {override}',
                file=sys.stderr,
                flush=True,
            )
    return DEFAULT_PORT


def run():
    port = resolve_port()
    address = ('', port)
    httpd = ThreadingHTTPServer(address, SpacePirateHTTPRequestHandler)
    print(f'Serving Space Pirate HQ on port {port}', flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('Shutting down server', flush=True)
    finally:
        httpd.server_close()


if __name__ == '__main__':
    run()
