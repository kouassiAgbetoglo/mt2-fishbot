import cv2 as cv
import numpy as np


class Filter():

    h_min = 0
    s_min = 0
    v_min = 0
    h_max = 0
    s_max = 0
    v_max = 0

    def __init__(self, hsv_values):
        self.h_min, self.s_min, self.v_min, self.h_max, self.s_max, self.v_max = hsv_values

    def hsv_filter(self, haystack_img):
        lower = np.array([self.h_min, self.s_min, self.v_min])
        upper = np.array([self.h_max, self.s_max, self.v_max])

        hsv = cv.cvtColor(haystack_img, cv.COLOR_BGR2HSV)
        mask = cv.inRange(hsv, lower, upper)
        output = cv.bitwise_and(haystack_img,haystack_img, mask= mask)

        return output