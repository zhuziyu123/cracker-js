import base64
import json
import os
import pprint
import re
import cv2
import requests
from 携程滑块.解密 import *
import numpy as np
from PIL import Image, ImageDraw
from 携程滑块.获取坐标 import *


def download_img(name, img):
    img_path = 'images/{}.jpg'.format(name)
    img = base64.b64decode(img)
    with open(img_path, 'wb') as fs:
        fs.write(img)


def draw_line(x, front_img_path):
    img = Image.open(front_img_path)
    img_draw = ImageDraw.Draw(img)
    img_draw.line((x, 0, x, img.size[1]), 'red')
    img.save(front_img_path.replace('.jpg', '.png'))


def tell_location(bg_img_path, front_img_path):
    img_rgb = cv2.imread(bg_img_path)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(front_img_path, 0)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    # 使用二分法查找阈值的精确值
    L = 0
    R = 1
    start = 0
    run = 1
    while run < 20:
        run += 1
        threshold = (R + L) / 2
        if threshold < 0:
            print('Error')
            return None
        loc = np.where(res >= threshold)
        if len(loc[1]) > 1:
            L += (R - L) / 2
        elif len(loc[1]) == 1:
            start = loc[1][0]
            break
        elif len(loc[1]) < 1:
            R -= (R - L) / 2
    distance = int(start)
    draw_line(distance, front_img_path)
    os.remove(front_img_path)
    os.remove(bg_img_path)
    return distance


class HK:
    def __init__(self):
        self.session = requests.session()
        self.session.headers = {
            'origin': 'https://flights.ctrip.com',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,'
                          ' like Gecko) Chrome/86.0.4240.75 Safari/537.36',
            'accept': '*/*',
            'referer': 'https://flights.ctrip.com/',
            'accept-language': 'zh-CN,zh;q=0.9',
        }
        self.ep = ""
        self.dim = ""

    def getToken(self):
        """
        获取 token
        :return:
        """
        url = 'https://m.ctrip.com/restapi/soa2/11470/getToken.json?t={}&callback=$_bf_uniq_F13'.format(
            int(time.time() * 1000))
        resp = self.session.get(url)
        token = re.search(r'data":{"token":"(\d+)",', resp.text).group(1)
        return token

    def risk_inspect(self, token):
        """
        获取 携程滑块图片
        :param token:
        :return:
        """
        url = 'https://ic.ctrip.com/captcha/v4/risk_inspect'
        self.ep = extend_param()
        self.dim = dimensions(token)
        _sign = 'appid=' + '100009556' + "&business_site=" + 'search_airticketscivil_online_pic' + \
                "&version=" + '2.0.4' + "&dimensions=" + self.dim + "&extend_param=" + self.ep
        params = {
            "callback": "captcha00899045683872961",
            "extend_param": self.ep,
            "appid": "100009556",
            "business_site": "search_airticketscivil_online_pic",
            "version": "2.0.4",
            "dimensions": self.dim,
            "sign": sign(_sign)
        }
        resp = self.session.get(url, params=params)
        _json = re.search(r'captcha00899045683872961\((.*?)\)', resp.text, re.DOTALL).group(1)
        _json = json.loads(_json)

        rid = _json['result']['rid']
        token = _json['result']['token']

        jigsaw_image = _json['result']['risk_info']['process_value']['jigsaw_image']
        processed_image = _json['result']['risk_info']['process_value']['processed_image']
        download_img('jigsaw_image', jigsaw_image)
        download_img('processed_image', processed_image)
        distance = tell_location('images/jigsaw_image.jpg', 'images/processed_image.jpg')
        return distance, token, rid

    def verify_track(self, token, rid, distance):
        """
        验证 轨迹
        携程对这个没有验证，即使错了也过
        :param token:
        :param rid:
        :param distance:
        :return:
        """
        url = 'https://ic.ctrip.com/captcha/v4/verify_jigsaw'
        verify_msg = hk_verify(distance)
        _sign = 'appid=100009556&business_site=search_airticketscivil_online_pic&version=2.0.4&verify_msg={}&' \
                'dimensions={}&extend_param={}&token={}&captcha_type=JIGSAW'.format(verify_msg, self.dim, self.ep,
                                                                                    token)
        params = {
            'callback': 'captcha02801029058423541',
            'appid': '100009556',
            'business_site': 'search_airticketscivil_online_pic',
            'token': token,
            'rid': rid,
            'version': '2.0.4',
            'verify_msg': verify_msg,
            'dimensions': self.dim,
            'extend_param': self.ep,
            'sign': sign(_sign),
        }
        resp = self.session.get(url, params=params)
        _json = re.search(r'captcha02801029058423541\((.*?)\)', resp.text, re.DOTALL).group(1)
        _json = json.loads(_json)
        rid = _json['result']['rid']
        token = _json['result']['token']

        big_image = _json['result']['risk_info']['process_value']['big_image']
        small_image = _json['result']['risk_info']['process_value']['small_image']
        download_img('big_image', big_image)
        download_img('small_image', small_image)
        return rid, token

    def verify_icon(self, token, rid):
        """
        点选验证码 需要获取3个坐标点
        没学过机器学习，不会，手动点
        :param token:
        :param rid:
        :return:
        """
        url = 'https://ic.ctrip.com/captcha/v4/verify_icon'
        img_p = Image_point()
        p = img_p.get_point()
        verify_msg = icon_verify(p)
        _sign = 'appid=100009556&business_site=search_airticketscivil_online_pic&version=2.0.4&verify_msg={}&' \
                'dimensions={}&extend_param={}&token={}&captcha_type=ICON'.format(verify_msg, self.dim, self.ep,
                                                                                  token)
        params = {
            'callback': 'captcha0005461717099524588',
            'appid': '100009556',
            'business_site': 'search_airticketscivil_online_pic',
            'token': token,
            'rid': rid,
            'version': '2.0.4',
            'verify_msg': verify_msg,
            'dimensions': self.dim,
            'extend_param': self.ep,
            'sign': sign(_sign),
        }
        resp = self.session.get(url, params=params)
        _json = re.search(r'captcha0005461717099524588\((.*?)\)', resp.text, re.DOTALL).group(1)
        _json = json.loads(_json)
        rid = _json['result']['rid']
        token = _json['result']['token']
        return rid, token

    def risk(self, rid, token):
        """
        验证
        出现滑块时 toWhiteMsg = success
        否则                 = fail
        :param rid:
        :param token:
        :return:
        """
        self.session.headers['content-type'] = 'application/json'
        url = 'https://flights.ctrip.com/itinerary/api/12808/eliminateRisk'
        data = {
            'businessSite': "search_airticketscivil_online_pic",
            'checkState': "success",
            'rid': rid,
            'token': token,
            'version': "2.0.4",
        }
        resp = self.session.post(url, data=json.dumps(data))
        content = resp.json()
        print(content)
        code = content['code']
        if code == 404:
            print('验证失败')
            return False
        if content['toWhiteMsg'] == 'Success':
            print('验证成功')
            return True
        else:
            print('验证失败')
            return False

    def start(self):
        tk = self.getToken()
        dis, t, r = self.risk_inspect(tk)
        time.sleep(random.uniform(0.1, 0.5))
        ri, to = self.verify_track(t, r, dis)
        rr, tt = self.verify_icon(to, ri)
        self.risk(rr, tt)


if __name__ == '__main__':
    xc = HK()
    xc.start()
