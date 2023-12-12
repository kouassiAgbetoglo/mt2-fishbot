from GetWindowList import *
from time import time
from windowCapture import WindowCapture
import cv2 as cv
import numpy as np
from vision import Vision
import os
from CONSTANT import *
from filter import Filter
from HSV_value import *

os.chdir(os.path.dirname(os.path.abspath(__file__)))


handler = WindowHandler()
hwnds = handler.hwnd_window_list('METIN2')
hwnd = hwnds[0]['hwnd']

wincap = WindowCapture(hwnd)


loop_time = time()

roi = (GAMEWINDOW_X, GAMEWINDOW_Y, GAMEWINDOW_W, GAMEWINDOW_H)
center = (FISHPOND_X + int(FISHPOND_W/2), FISHPOND_Y + int(FISHPOND_H/2))
radius = FISHPOND_W//2
circular_mask = {'center': center,
                 'radius': radius}

###

fish_game = Vision('images\gameWindow.png')
game_hsv_filter = Filter((H_MIN, S_MIN, V_MIN, H_MAX, S_MAX, V_MAX))

fish = Vision('images\ish.png')



fish_game_roi = []

#cascade_fish = cv.CascadeClassifier('cascade/cascade.xml')

while(True):
    # get an updated image of the game
    screenshot = wincap.get_screenshot()

    if not fish_game_roi:
        fish_game_roi = fish_game.find(screenshot, threshold=0.5, debug_mode=None, mask=None)
        game_circle_roi = fish_game.get_center(fish_game_roi)
    else:
        c_x, c_y, _ = game_circle_roi
        game_radius = radius-9
        masked_image = fish_game.circular_mask(screenshot, (c_x, c_y), game_radius)
        filtered_screenshot = game_hsv_filter.hsv_filter(masked_image)
        fish.find(filtered_screenshot, threshold=0.4, debug_mode='rectangles', mask=None)


    #cv.imshow('Raw', screenshot)
    
    # debug the loop rate

    loop_time = time


    # press 'q' with the qoutput window focused to exit.
    # waits 1 ms every loop to process key presses

    key = cv.waitKey(1)
    if key == ord('q'):
        cv.destroyAllWindows()
        break
    """elif key == ord('f'):
        cv.imwrite('positive/' + str(i) + '.jpg', screenshot)
    elif key == ord('d'):
        cv.imwrite('negative/'+ str(i) + '.jpg', screenshot)"""

print('Done.')