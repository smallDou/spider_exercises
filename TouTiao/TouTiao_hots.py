#coding=utf-8
#今日头条
from lxml import etree
import requests
import json


def get_url():
    url = 'https://www.toutiao.com/api/pc/focus/'
    headers = {
        'accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding':
        'gzip, deflate, br',
        'accept-language':
        'zh-CN,zh;q=0.9',
        'cache-control':
        'max-age=0',
        'cookie':
        'UM_distinctid=15fcf3cf60ca0-0288dff71f1233-3e63430c-144000-15fcf3cf60d9a1; uuid="w:ed90ee72a3c84a5386d8a0385cf3e8b6"; _ga=GA1.2.1812818719.1511010395; WEATHER_CITY=%E5%8C%97%E4%BA%AC; __tea_sdk__user_unique_id=76350642421; uid_tt=4488d878f6aa105d2aab379854780129; __tea_sdk__web_id=3311496932; __tea_sdk__ssid=0; odin_tt=2c1b5594fed454d4f529a2c869ac0968eb26760c1a59a8c0acba9e9ef4e3e3c40bdd0ac0cdb1ba4f56bcddf8f8f82ca4; tt_webid=6527949476766008840; __tasessionId=nc8i15hqi1520229078681; CNZZDATA1259612802=1057392987-1511006566-%7C1520227366; tt_webid=6527949476766008840; sso_login_status=0; login_flag=9fbb1e1d9a566e4399d54c73efa8d36a; sessionid=0750f6476499a79e8d00b1c2f8a2ff3f; sid_tt=0750f6476499a79e8d00b1c2f8a2ff3f; sid_guard="0750f6476499a79e8d00b1c2f8a2ff3f|1520230291|15552000|Sat\054 01-Sep-2018 06:11:31 GMT',
        'referer':
        'https://www.toutiao.com/',
        'upgrade-insecure-requests':
        '1',
        'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.encoding = 'utf8'
    print(response.status_code)
    html = response.text
    data = json.loads(html)
    print(data)


if __name__ == '__main__':
    count = 0
    get_url()