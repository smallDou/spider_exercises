import requests
import json
import re
from urllib.parse import urlencode
URL = 'https://v.qq.com/x/page/e0618mwd2zc.html'

##尝试cookies，果然没用,而且cookie一直在变化
headers = {
    'user-agent':
    'Mozilla/5.0 (Linux; U; Android 4.0.4; en-gb; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
    #'cookie': 'eas_sid=i1e5U066C9k7o3r791i0j1S5i3; pgv_pvi=5036492800; LW_uid=R1P510a669C7d3w7r9h2R4w1G5; RK=Y+OixzSvOY; pgv_pvid_new=1136116080_15791654674; tvfe_boss_uuid=d0ddad999be51822; gr_user_id=c0626df4-b200-43cf-884a-86eda1234e22; ue_uid=043dd91c833cecd3623ce0994addef34; ue_ts=1512226282; ue_uk=69acddeeedde1bcff34ba2d4aebfa2e6; ue_skey=9b0880b3185434408b2c1664fb8fb322; ptcz=e6083b59a8b3d46dbb87e01f50e1a7b07305d5c0269e2c02d25e648898197806; pgv_pvid=2218299800; appuser=AEAA23274D2553F0; o_minduid=sIog481dQ_-SwIsDa9jrqFQfbLUg9fEA; LW_sid=v1D5A1D410V381i1s3l7h4D2H0; pac_uid=1_1136116080; OUTFOX_SEARCH_USER_ID_NCOO=1854117588.1482818; adid=1136116080; luin=o1136116080; lskey=000100009532d4c4ac31fc5e91bccd9b51342f47dca0a2e315530461533b8e2e7a1bcc71213595ae71ec3568; pgv_si=s2950734848; ptisp=cm; _qpsvr_localtk=0.9163413758105432; ptui_loginuin=1411605350; pgv_info=ssid=s3135979664; pt2gguin=o1136116080; uin=o1136116080; o_cookie=1136116080; logout_page=; qm_authimgs_id=0; LBSturn=736; image_md5=1b414156d4fa4fa1b1387cf98079b0b8; qm_verifyimagesession=h016ff1163a3d61d9b2530e6ad8da30443fda6fb1c73904adb011866d43349c30d128d49c05024476dc; uid=800271461; LZTturn=988; ufc=r47_4_1525009353_1524987344; cm_cookie=V1,10027&1508779887198146&AQEBRIZokb9KZptRXzaJqG2B1EUlQOll7Aac&171101&171101,10008&zIfrWQoAA7RKwTkAAQHiQ70N&AQEBRIZokb9KZpsNbi1MtHRV6fhlcm16F7jw&171022&171106,110146&5766155220301719518&AQEBRIZokb9KZpuqQhoxv5WxtWDykXve8kuW&171123&171123,110120&5766155220301719518&AQEBRIZokb9KZptJV1wMea3TcaM8YeCtOVwa&171208&171208,110087&xoxlVSOrQ_O575vG5WCiLVn4O6c&AQEBRIZokb9KZpvd99uk2YsmJy5mXtejFojx&171101&180117,110069&3e99f585f473c&AQEBRIZokb9KZpuquCP5Zh7tTqJ9yNJjVkuu&171107&180309,110080&44F78ED30CA74D59FB449C&AQEBRIZokb9KZptKJI2rfJVa0cuGOQ6PVJr8&171123&180317,10045&0&AQEBRIZokb9KZpvXdiYicB_VOHiysdYCHC7q&171104&180327,10016&G1LIOs21cjIy&AQEBRIZokb9KZptDA6YZM7yLU17jpw4yhYuw&180322&180412,110066&Trx5e0umd350&AQEBRIZokb9KZptat7syLwp-D1Hle8LiHYbQ&171031&180419,110065&6NQb99fzsL&AQEBRIZokb9KZpuRcIaEp4v2bqcBAF5JSObX&171022&180419,110061&6b170ef215cd50e&_Fne0fHeJeT6-H5QGbr0BbpNKr94RNPs2L759hAFy_aSiYCKAQqVEWgjGHCFhVAC&180420&180420,110055&s0e909e63aa504946e8&AQEBRIZokb9KZptTKkCWC_k_PljMEdhb9xUw&171031&180428,110064&24hGd016uR87&AQEBRIZokb9KZpvVmmbEQzFaIJp-PosWZxEI&171123&180429; mobileUV=1_16311229a52_dbee6; skey=@oi9cgGBk7; LHTturn=1014; LWHturn=137; LWKturn=250; LWIturn=111; LPPBturn=627; LZIturn=217; LKBturn=822; LPVLturn=303; LVMturn=1042; Lturn=907; LTPturn=985; psessionid=cac5e4d0_1525016266_1136116080_26236; lv_play_indexl.=11; psessiontime=1525016273',
}

def get_vid(url):
    response = requests.get(url)
    html = response.text
    href = re.search(r'<link rel="canonical" href="(.*?)"', html).group(1)
    ht = href.split('/')[-1]
    vid = re.search(r'(.*?).html', ht).group(1)
    return vid


def get_info_url(vid):
    # 默认的参数
    data = {
        'vid': vid,
        'otype': 'json',
        'platform': '2350201',
        'guid': 'ac494dbb8d4821d1e79e821cf7782cf9',
        'sdtfrom': 'v1095',
        '_qv_rmt': 'WpkBmSmwA120893Am=',
        '_qv_rmt2': 'qaNK93R+155086MVQ=',
    }
    # getinfo的base_url
    base_info_url = 'https://h5vv.video.qq.com/getinfo'
    # format方法生成getinfo
    params = urlencode(data)
    info_url = base_info_url + '?' + params
    return info_url


def get_keys(info_url):
    response = requests.get(info_url, headers=headers)
    pattern = re.compile(r'(\{.*\})')  #使用贪婪匹配
    data = re.search(pattern, response.text).group(1)
    data = json.loads(data)
    for each in data.get('vl').get('vi'):
        fvkey = each.get('fvkey')
        fn = each.get('fn')
        self_host = each.get('ul').get('ui')[0].get('url')
        keys = {'fvkey': fvkey, 'fn': fn, 'self_host': self_host}
        return keys


def get_real_url(keys):
    # 真实地址的base_url
    base_real_url = '{self_host}{fn}?vkey={fvkey}'
    # 组装视频真实地址
    real_url = base_real_url.format(
        self_host=keys['self_host'], fn=keys['fn'], fvkey=keys['fvkey'])
    return real_url


def main():
    vid = get_vid(URL)
    info_url = get_info_url(vid)
    print(info_url)
    keys = get_keys(info_url)
    print(keys)
    print(get_real_url(keys))


if __name__ == '__main__':
    main()