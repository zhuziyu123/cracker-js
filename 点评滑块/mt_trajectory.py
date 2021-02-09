import random
import time

ts = int(time.time() * 1000)
add = 5000 + random.randint(10, 350)
cts = int(time.time() * 1000) + add


def generate_trajectory(distance):
    tracks_list = []
    timestamp_list = []
    y_list = []

    # 当前位移
    current = 855
    # 减速阈值
    # mid = distance * 9/10
    # 计算间隔
    t = 1.2
    # 初速度
    v = 0

    while current < distance:
        # if current < mid:
        # 加速度为正 2
        a = 2
        # else:
        #     加速度为负 3
        # a = -3
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

    timestamp = add
    for i in range(len(tracks_list)):
        t = timestamp + random.randint(10, 20)
        timestamp = t
        timestamp_list.append(timestamp)

    for j in range(len(tracks_list)):
        y = random.choice(
            [0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1, -1, -2, -2, -2, -2, -3, -3])
        if j < 4:
            y_list.append(0)
        else:
            y_list.append(y)
    trace = []
    for index, x in enumerate(tracks_list):
        trace.append([0, x, 260 - y_list[index], timestamp_list[index]])
    return trace


def get_data():
    point = generate_trajectory(1058)
    data = {
        "trajectory": [
            {
                "point": point
            }
        ],
        "env": {
            "zone": [
                230,
                33
            ],
            "client": [
                844,
                243.5
            ],
            "Timestamp": [
                ts,
                cts
            ],
            "count": 1,
            "timeout": 1
        }
    }
    return data
