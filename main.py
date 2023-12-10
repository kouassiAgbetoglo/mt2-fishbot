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

wincap = WindowCapture(hwnd)

spell = Vision('spell.PNG')
##

loop_time = time()

roi = (GAMEWINDOW_X, GAMEWINDOW_Y, GAMEWINDOW_W, GAMEWINDOW_H)
center = (FISHPOND_X + int(FISHPOND_W/2), FISHPOND_Y + int(FISHPOND_H/2))
radius = FISHPOND_H//2
circular_mask = {'center': center,
                 'radius': radius}

while(True):
    # get an updated image of the game
    screenshot = wincap.get_screenshot()

    # debug the loop rate
    """print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()"""

    spell.draw_game(screenshot, roi) # a modifier
    spell.find(screenshot, 0.7, 'rectangles', circular_mask)

    # press 'q' with the qoutput window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')