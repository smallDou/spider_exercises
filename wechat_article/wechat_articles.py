import requests
from urllib.parse import urlencode
from pyquery import PyQuery as pq

KEYWORD = '美食'

MAX_COUNT = 15

base_url = 'http://weixin.sogou.com/weixin?'

PROXY_POOL_URL = 'http://localhost:5000/get'

headers = {
    'Cookie':
    'CXID=71B83BCE65B914F7E9336F0227E0F444; SUID=94F78ED33765860A59E0E29800097EF6; SUV=00414ADC3A14E8695A18454CC0A32381; IPLOC=CN4303; ld=rZllllllll2zBs4clllllV$UCTUlllll30VHmkllll9lllllpZlll5@@@@@@@@@@; LSTMV=188%2C300; LCLKINT=2980; ad=JZllllllll2zr2BQlllllV$7COYlllllTsn6akllll9lllll9qxlw@@@@@@@@@@@; ABTEST=4|1521883289|v1; weixinIndexVisited=1; JSESSIONID=aaaNWWu_7zyv5e8uGMOiw; ppinf=5|1521962063|1523171663|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToxOlF8Y3J0OjEwOjE1MjE5NjIwNjN8cmVmbmljazoxOlF8dXNlcmlkOjQ0Om85dDJsdUFkclFyU0dONU1idTY2dmlUN3dDVU1Ad2VpeGluLnNvaHUuY29tfA; pprdig=O2GvMg2xSUkoC2rc0Pj0qm2uObovrGlH4uzRB19_A8IjH0Fp47ZK_3IzznlayvPOPUkAgDKcROmPH0Pq6cXKtTycwqDeyplmGw6RINOdDkrjkGvA7kerxODyNMhLgT3eqORud1au6Sehd8csJ5RMrIfewrjNZ-u0esVf2l0zyWg; sgid=15-34245489-AVq3TEicIuCOCCjFDVFn0re8; PHPSESSID=209qnl2584tbvrb4u7jt7bf4n3; SUIR=B6A1198852563B76428A18E65342C7FA; SNUID=0F18A130EBEF82D285658126EB32099A; sct=5; ppmdig=15219892130000009f165c3f46e7c1a7404ba3d9547bfb7e',
    'Host':
    'weixin.sogou.com',
    'Upgrade-Insecure-Requests':
    '1',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
}

proxy = None


def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        print('Get Proxy Error')


def get_url(keyword, page):
    data = {'query': keyword, 'type': 2, 'page': page}
    queries = urlencode(data)
    url = base_url + queries
    return url


def get_index_page(url, count=1):  #count计算请求线程池数量，避免线程池崩溃
    global proxy
    if count >= MAX_COUNT:
        print('Tried Too Many Counts')
        return None
    try:
        if proxy:
            proxies = {'http': 'http://' + proxy}
            response = requests.get(
                url, allow_redirects=False, headers=headers, proxies=proxies)
        else:
            response = requests.get(
                url, allow_redirects=False, headers=headers)
        if response.status_code == 200:
            return response.text
        if response.status_code == 302 or response.status_code == 301:
            print('302')
            count += 1
            proxy = get_proxy()
            print('Using proxy:%s' % proxy)
            return get_index_page(url, count)
        else:
            print(response.status_code)
            print('Get_Index_Page Error')
    except TimeoutError:
        count += 1
        proxy = get_proxy()
        return get_index_page(url, count)


def parse_index_page(html):
    doc = pq(html)
    urls = doc('.news-box .news-list li .txt-box h3 a').items()
    for url in urls:
        yield url.attr('href')


def get_details(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except ConnectionError:
        print('Get_Detail Error')


def parse_details(html):
    try:
        doc = pq(html)
        title = doc('#activity-name').text()
        date = doc('#post-date').text()
        nickname = doc('#post-user').text()
        wechat = doc('#js_profile_qrcode > div > p:nth-child(3) > span').text()
        return {
            'title': title,
            'date': date,
            'nickname': nickname,
            'wechat': wechat
        }
    except Exception:
        return None


def main():
    for page in range(1, 101):
        print(page)
        index_url = get_url(KEYWORD, page)
        index_html = get_index_page(index_url)
        for article_url in parse_index_page(index_html):
            print(article_url)
            article_html = get_details(article_url)
            result = parse_details(article_html)
            print(result)


if __name__ == '__main__':
    main()