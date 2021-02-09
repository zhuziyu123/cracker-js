import cv2
import numpy as np


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
    return distance
