import requests
from bs4 import BeautifulSoup

URL = 'https://finance.naver.com/sise/sise_market_sum.naver?sosok=0&page=1'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/124.0.0.0 Safari/537.36',
                  'Cache-Control': 'no-cache',
}
SELECTOR = 'table.type_2 tbody tr' 

def main() -> None:
    resp = requests.get(URL, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    resp.encoding = 'euc-kr'  

    soup = BeautifulSoup(resp.text, 'html.parser')

    rows = soup.select(SELECTOR) 
    items = []
    for tr in rows:
        tds = tr.find_all('td')
        if len(tds) < 10:
            continue  

        name_el = tds[1].select_one('a')
        price_el = tds[2]
        volume_el = tds[9]
        mcap_el = tds[6]

        name = name_el.get_text(strip=True) if name_el else ''
        price = price_el.get_text(strip=True)
        volume = volume_el.get_text(strip=True)
        mcap = mcap_el.get_text(strip=True)

        if name:
            items.append({
                'name': name,
                'price': price,
                'volume': volume,
                'market_cap': mcap,
            })

    print(items)

if __name__ == '__main__':
    main()
