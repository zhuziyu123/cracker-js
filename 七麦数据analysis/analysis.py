import base64
import time

import requests


def S(_s):
    return base64.b64encode(_s.encode()).decode()


def u(n):
    return chr(n)


def j(t, n):
    t = list(t)
    a = len(t)
    e = len(n)
    for s in range(0, a):
        t[s] = u(ord(t[s][0]) ^ ord(n[(s + 10) % e][0]))
        s += 1
    return ''.join(t)


def analysis(url, params):
    new_params = []
    for key in params:
        new_params.append(params[key])
    D = 1388
    r = int(time.time() * 1000) - D - 1515125653845
    new_params.sort()
    i = ''.join(new_params)
    i = S(i)
    i += "@#" + url.replace("https://api.qimai.cn", '')
    i += "@#" + str(r)
    i += "@#" + str(1)
    s = S(j(i, "00000008d78d46a"))
    return s


url = 'https://api.qimai.cn/rank/indexPlus/brand_id/0'
params = {
    'brand': 'all',
    'country': 'cn',
    'device': 'iphone',
    'genre': '36',
    'date': '{}'.format(time.strftime("%Y-%m-%d", time.localtime())),
    'page': '1'
}
params['analysis'] = analysis(url, params)
print(params['analysis'])
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
