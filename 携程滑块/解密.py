import random
import time

import execjs

with open('crypto.js', 'r', encoding='utf-8') as f:
    js_code = f.read()

with open('sfp.js', 'r', encoding='utf-8') as f:
    sfp_js = f.read()

ctx = execjs.compile(js_code)
sfp_ctx = execjs.compile(sfp_js)


def extend_param():
    return ctx.call('crypto_encrypt', {"resolution_width": 1920, "resolution_height": 1080, "language": ""})


def dimensions(token):
    environment = {
        "rt": "fp=11ln61j-cbn4nq-1oi8kq&vid=1612340500830.3mzbq7&pageId=10320606143&r=b771e64494e943f391d5d2a7eaecdedb"
              "&ip=*********"  # ip
              "&rg=undefined&kpData=0_0_0&kpControl=0_0_0-0_0_0&kpEmp=0_0_0_0_0_0_0_0_0_0-0_0_0_0_0_0_0_0_0_0"
              "-0_0_0_0_0_0_0_0_0_0&screen=1920x1080&tz=+8&blang=zh-CN&oslang=zh-CN&ua=Mozilla%2F5.0%20(Window"
              "s%20NT%2010.0%3B%20WOW64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F78.0.3904"
              ".108%20Safari%2F537.36&d=flights.ctrip.com&v=25&kpg=0_0_0_0_0_0_0_0_0_0&adblock=F&cck=F",
        "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        "p": "pc",
        "fp": "11ln61j-cbn4nq-1oi8kq",  #
        "vid": "1612340500830.3mzbq7",  #
        "sfp": sfp_ctx.call('sfp', token),  #
        "identify": "aWJ0jQ5ZLJ+Bmc+Xk7n7hXh63N/cY9a3Jgcgjl+aC4xg=",  #
        "svid": "QfwBEZ%24Bz%7BC%2CAG%7C~y%7CBFC%26%5D%5C'L",  #
        "guid": None,
        "h5_duid": None,
        "pc_duid": None,
        "hb_uid": None,
        "pc_uid": None,
        "h5_uid": None,
        "infosec_openid": None,
        "device_id": "1.5",  # cookie _bfs
        "client_id": "p1=10320606143&p2=10320673302&v1=5&v2=4",  # cookie _bfi
        "pid": ctx.call('random', 16, 2, "corpid"),  # 生成
        "sid": ctx.call('random', 16, 1, "SMBID"),  # 生成
        "login_uid": ctx.call('random', 10, 2, "login_uid"),  # 生成
        "client_type": "PC",
        "site": {
            "type": "PC",
            "url": "https://flights.ctrip.com/itinerary/oneway/bjs-sha",
            "ref": "",
            "title": "北京到上海机票查询预订-北京飞上海特价机票价格-携程飞机票",
            "keywords": "北京到上海机票,北京到上海飞机票,北京到上海特价机票,携程飞机票"
        },
        "device": {
            "width": 1920,
            "height": 1080,
            "os": "",
            "pixelRatio": 1,
            "did": ""
        },
        "user": {
            "tid": "",
            "uid": "",
            "vid": ""
        }
    }
    return ctx.call('crypto_encrypt', environment)


def hk_verify(distance):
    trajectory = {"st": int(time.time() * 1000), "slidingTime": random.randint(1000, 1500), "display": "1920x1080",
                  "keykoardTrack": [],
                  "slidingTrack": generate_trajectory(distance),
                  "timezone": -480, "flashState": False,
                  "language": "zh-CN", "platform": "Win32", "cpuClass": None, "hasSessStorage": True,
                  "hasLocalStorage": True,
                  "hasIndexedDB": True, "hasDataBase": True, "doNotTrack": False, "touchSupport": False,
                  "mediaStreamTrack": True,
                  "value": int(distance / 280 * 300)}
    return ctx.call('crypto_encrypt', trajectory)


def generate_trajectory(distance):
    tracks_list = []
    timestamp_list = []
    y_list = []

    # 当前位移
    current = 4
    # 减速阈值
    mid = distance * 4 / 5
    # 计算间隔
    t = 0.2
    # 初速度
    v = 0

    while current < distance:
        if current < mid:
            # 加速度为正 2
            a = 2
        else:
            # 加速度为负 3
            a = -3
        # 初速度 v0
        v0 = v
        # 当前速度 v = v0 + at
        v = v0 + a * t
        # 移动距离 x = v0t + 1/2 * a * t^2
        move = v0 * t + 1 / 2 * a * t * t
        # 当前位移
        current += move
        # 加入轨迹
        tracks_list.append(round(current))

    timestamp = 0
    for i in range(len(tracks_list)):
        t = 10 + random.randint(5, 10)
        timestamp += t
        timestamp_list.append(timestamp)

    for j in range(len(tracks_list)):
        y = random.choice(
            [766, 766, 766, 766, 766, 766, 767, 767, 767, 767, 767, 767, 767, 767, 767, 768, 768, 768])
        y_list.append(y)
    trace = []
    for index, x in enumerate(tracks_list):
        trace.append({'x': x + 830, 'y': y_list[index]})
    return trace


def icon_verify(point):
    st = int(time.time() * 1000)
    inputStartTs = st + random.randint(1000, 9000)
    inputEndTs = inputStartTs + random.randint(6000, 12000)
    inputTime = inputEndTs - inputStartTs
    icon = {
        "st": st,
        "display": "1920x1080",
        "keykoardTrack": [],
        "timezone": -480,
        "flashState": False,
        "language": "zh-CN",
        "platform": "Win32",
        "hasSessStorage": True,
        "hasLocalStorage": True,
        "hasIndexedDB": True,
        "hasDataBase": True,
        "doNotTrack": False,
        "touchSupport": False,
        "mediaStreamTrack": True,
        "value": point,
        "inputStartTs": inputStartTs,
        "inputEndTs": inputEndTs,
        "inputTime": inputTime,
        "selectMoveTrace": "[{\"x\":445,\"y\":594},{\"x\":518,\"y\":661},{\"x\":479,\"y\":733},{\"x\":484,\"y\":609},{\"x\":521,\"y\":637},{\"x\":515,\"y\":637},{\"x\":511,\"y\":637},{\"x\":505,\"y\":637},{\"x\":500,\"y\":637},{\"x\":495,\"y\":637},{\"x\":490,\"y\":637},{\"x\":484,\"y\":639},{\"x\":480,\"y\":640},{\"x\":476,\"y\":640},{\"x\":472,\"y\":642},{\"x\":469,\"y\":644},{\"x\":466,\"y\":646},{\"x\":464,\"y\":648},{\"x\":463,\"y\":650},{\"x\":461,\"y\":653},{\"x\":460,\"y\":655},{\"x\":459,\"y\":657},{\"x\":458,\"y\":659},{\"x\":457,\"y\":661},{\"x\":456,\"y\":662},{\"x\":455,\"y\":663},{\"x\":454,\"y\":664},{\"x\":452,\"y\":665},{\"x\":451,\"y\":665},{\"x\":450,\"y\":665},{\"x\":448,\"y\":666},{\"x\":447,\"y\":666}]&[{\"x\":520,\"y\":636},{\"x\":514,\"y\":637},{\"x\":507,\"y\":639},{\"x\":500,\"y\":639},{\"x\":494,\"y\":640},{\"x\":487,\"y\":640},{\"x\":483,\"y\":641},{\"x\":477,\"y\":642},{\"x\":471,\"y\":642},{\"x\":466,\"y\":642},{\"x\":460,\"y\":642},{\"x\":453,\"y\":644},{\"x\":447,\"y\":645},{\"x\":440,\"y\":646},{\"x\":436,\"y\":646},{\"x\":430,\"y\":647},{\"x\":423,\"y\":649},{\"x\":417,\"y\":649},{\"x\":411,\"y\":650},{\"x\":406,\"y\":651},{\"x\":399,\"y\":652},{\"x\":394,\"y\":652},{\"x\":390,\"y\":654},{\"x\":386,\"y\":655},{\"x\":384,\"y\":656},{\"x\":380,\"y\":659},{\"x\":378,\"y\":660},{\"x\":376,\"y\":661},{\"x\":375,\"y\":663},{\"x\":374,\"y\":665},{\"x\":374,\"y\":666},{\"x\":373,\"y\":667},{\"x\":371,\"y\":668},{\"x\":370,\"y\":669},{\"x\":369,\"y\":670},{\"x\":367,\"y\":671},{\"x\":366,\"y\":672},{\"x\":366,\"y\":674},{\"x\":365,\"y\":675},{\"x\":363,\"y\":677},{\"x\":363,\"y\":678},{\"x\":362,\"y\":679},{\"x\":365,\"y\":679},{\"x\":366,\"y\":679},{\"x\":367,\"y\":680},{\"x\":367,\"y\":681},{\"x\":365,\"y\":684},{\"x\":364,\"y\":685},{\"x\":362,\"y\":686},{\"x\":360,\"y\":687},{\"x\":358,\"y\":688},{\"x\":357,\"y\":689},{\"x\":356,\"y\":690},{\"x\":355,\"y\":690},{\"x\":354,\"y\":691}]",
        "selectMoveTime": "{}&{}".format(random.randint(10000, 50000), random.randint(1000, 5000)),
        "selectCancelCount": 0,
        "selectIsTruncation": False
    }
    return ctx.call('crypto_encrypt', icon)


def sign(data):
    return ctx.call('md5', data)
