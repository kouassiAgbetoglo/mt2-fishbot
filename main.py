from GetWindowList import *
from time import time
from WindowCapture import WindowCapture
import cv2 as cv
import numpy as np

handler = WindowHandler()
hwnds = handler.hwnd_window_list('METIN2')
hwnd = '331192'

print(hwnd)

wincap = WindowCapture(hwnd)
##
loop_time = time()

while(True):
    # get an updated image of the game
    screenshot = wincap.get_screenshot()

    cv.imshow('Computer Vision', screenshot)

    # debug the loop rate
    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    # press 'q' with the qoutput window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')