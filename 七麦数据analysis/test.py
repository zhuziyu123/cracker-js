import time

import requests
import execjs

with open('analysis.js', 'r', encoding='utf-8') as f:
    js_code = f.read()
ctx = execjs.compile(js_code)
url = 'https://api.qimai.cn/rank/indexPlus/brand_id/0'
params = {
    'brand': 'all',
    'country': 'cn',
    'device': 'iphone',
    'genre': '36',
    'date': '{}'.format(time.strftime("%Y-%m-%d", time.localtime())),
    'page': '1'
}
new_params = []
for key in params:
    new_params.append(params[key])

analysis = ctx.call('analysis', url, new_params)
params['analysis'] = analysis
headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'referer': 'https://www.qimai.cn/rank',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
}
resp = requests.get(url, params=params, headers=headers)
print(resp.json())