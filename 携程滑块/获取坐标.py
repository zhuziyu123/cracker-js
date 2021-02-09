import cv2


class Image_point:

    def __init__(self):
        self.big_image = cv2.imread('images/big_image.jpg')
        self.small_image = cv2.imread('images/small_image.jpg')
        cv2.namedWindow('small_image', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('small_image', self.small_image)
        self.point = []

    def On_EVENT_BUTTON_DOWN(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            xy = "%d,%d" % (x, y)
            cv2.circle(self.big_image, (x, y), 1, (255, 0, 0), thickness=-1)
            cv2.putText(self.big_image, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                        1.0, (0, 0, 0), thickness=1)
            self.point.append(x)
            self.point.append(y)
            cv2.imshow("big_image", self.big_image)

    def get_point(self):
        cv2.namedWindow("big_image")
        cv2.setMouseCallback("big_image", self.On_EVENT_BUTTON_DOWN)
        while True:
            cv2.imshow("big_image", self.big_image)
            if cv2.waitKey(0) & 0xFF == 27:
                break
        cv2.destroyAllWindows()
        return self.point
