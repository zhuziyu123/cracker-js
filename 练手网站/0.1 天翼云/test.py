# 天翼云
# des
# 登录加密
# https://m.ctyun.cn/wap/main/auth/login?redirect=%2Fmy
import time

import execjs
import requests

with open('test.js', 'r', encoding='utf-8') as f:
    js_code = f.read()
ctx = execjs.compile(js_code)
p = ctx.call('params', '1123123sadd23', '123123')
headers = {
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Accept': 'application/json, text/plain, */*',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Mobile Safari/537.36',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://m.ctyun.cn/wap/main/auth/login?redirect=%2Fmy',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

params = {
    'userName': '123123',
    'password': p['password'],
    'referrer': 'wap',
    'mainVersion': '300021100',
    'comParam_curTime': int(time.time() * 1000),
    'comParam_seqCode': p['comParam_seqCode'],
    'comParam_signature': p['comParam_signature'],
    'isCheck': 'true',
    'locale': 'zh-cn',
}

response = requests.get('https://m.ctyun.cn/account/login', headers=headers, params=params)
print(response.text)
