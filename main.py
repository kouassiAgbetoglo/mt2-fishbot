from GetWindowList import *
from time import time
from WindowCapture import WindowCapture
import cv2 as cv
import numpy as np
from vision import Vision
import os
from CONSTANT import *

os.chdir(os.path.dirname(os.path.abspath(__file__)))


handler = WindowHandler()
hwnds = handler.hwnd_window_list('METIN2')
hwnd = hwnds[0]['hwnd']

print(hwnd)

wincap = WindowCapture(hwnd)

clock = Vision('clock.png')
fishCount = Vision('fishCount.PNG')
fishPond = Vision('fishPond.PNG')
fish = Vision('fish.png')
##

loop_time = time()

roi = (GAMEWINDOW_X, GAMEWINDOW_Y, GAMEWINDOW_W, GAMEWINDOW_H)
       
while(True):
    # get an updated image of the game
    screenshot = wincap.get_screenshot()

    #cv.imshow('Computer Vision', screenshot)

    # debug the loop rate
    """print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()"""

    clock.draw_game(screenshot, roi) # a modifier
    fishCount.find(screenshot, 0.7, 'rectangles', roi)
    clock.find(screenshot, 0.7, 'rectangles', roi)
    fish.find(screenshot, 0.7, 'points', roi)
    point = fishPond.find(screenshot, 0.7, 'points', roi)
    print(point)

    # press 'q' with the qoutput window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')