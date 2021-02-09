import requests
import execjs
from 美团滑块.mt_trajectory import *

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Host': 'verify.meituan.com',
    'Pragma': 'no-cache',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',

}

with open('js/mthk.js', 'r', encoding='utf-8') as f:
    js_code = f.read()
ctx = execjs.compile(js_code)

session = requests.session()


def get_validation(requestCode):
    url = 'https://verify.meituan.com/v2/ext_api/page_data'
    data = {
        'requestCode': requestCode,
        'feVersion': '1.4.1',
        'source': '1',
    }
    resp = session.post(url, data=data, headers=headers)
    sess = resp.json()['data']['session']
    sign = resp.json()['data']['sign']
    request_code = resp.json()['data']['request_code']
    return sess, sign, request_code


def validation(requestCode):
    d = get_data()
    sess, sign, request_code = get_validation(requestCode)
    result = ctx.call('behavior_token', sess, sign, request_code, d)
    url = 'https://verify.meituan.com/v2/ext_api/spiderindefence/verify'
    data = {
        'id': 71,
        'request_code': request_code,
        'behavior': result['behavior'],
        'fingerprint': '',
        '_token': result['token']
    }
    resp = requests.post(url, data=data, headers=headers)
    print(resp.text)
    return resp.json()['data']['response_code']


validation('3eb269119a95420d9e03e4c0747f409c')
