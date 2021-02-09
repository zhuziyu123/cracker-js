import cv2


def FindPic(target, template):
    """
    找出图像中最佳匹配位置
    :param target: 目标即背景图
    :param template: 模板即需要找到的图
    :return: 返回最佳匹配及其最差匹配和对应的坐标
    """
    target_rgb = cv2.imread(target)
    target_gray = cv2.cvtColor(target_rgb, cv2.COLOR_BGR2GRAY)
    template_rgb = cv2.imread(template, 0)
    res = cv2.matchTemplate(target_gray, template_rgb, cv2.TM_CCOEFF_NORMED)
    value = cv2.minMaxLoc(res)
    x1 = value[0]
    x2 = value[1]
    p1 = value[2]
    p2 = value[3]
    print(value)
    if abs(float(x1)) > abs(float(x2)):
        return p1[0]
    else:
        return p2[0]
