import requests
from bs4 import BeautifulSoup

URL = 'https://news.kbs.co.kr/news/pc/main/main.html'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/124.0.0.0 Safari/537.36',
                  'Cache-Control': 'no-cache',
}
SELECTOR = 'a.box-content p.title' 


def main() -> None:
    resp = requests.get(URL, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    resp.encoding = 'utf-8'


    soup = BeautifulSoup(resp.text, 'html.parser')

    titles = []
    for el in soup.select(SELECTOR): 
        text = el.get_text(separator=' ', strip=True)
        if text:
            titles.append(text)

    print(titles)


if __name__ == '__main__':
    main()
