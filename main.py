from GetWindowList import *
from time import time, sleep
from windowCapture import WindowCapture
import cv2 as cv
import numpy as np
from vision import Vision
import os
from CONSTANT import *
from filter import Filter
from HSV_value import *
import pydirectinput


def send_key(hwnd, key=None):
        if key:
            pydirectinput.keyDown(key)
            pydirectinput.keyUp(key)

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    handler = WindowHandler()
    hwnds = handler.hwnd_window_list('METIN2')
    hwnd = hwnds[0]['hwnd']
    win32gui.SetForegroundWindow(hwnd)
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

    cpt = 0
    cpt_max = 2
    fish_game_roi = []

    time_fish_prev = 0
    time_fish = 0



    while(True):
        # get an updated image of the game
        screenshot = wincap.get_screenshot()

        fish_game_roi = fish_game.find(screenshot, threshold=0.5, debug_mode=None, mask=None)
        
        if fish_game_roi:
            game_circle_roi = fish_game.get_center(fish_game_roi)
            c_x, c_y, _ = game_circle_roi
            game_radius = radius-5
            masked_image = fish_game.circular_mask(screenshot, (c_x, c_y), game_radius)
            filtered_screenshot = game_hsv_filter.hsv_filter(masked_image)
            print(fish.detect(filtered_screenshot))
            """got_fish = fish.find(filtered_screenshot, threshold=0.4, debug_mode='rectangles', mask=None, info = False)
            time_fish_prev = time_fish
            if got_fish:
                time_fish = time()
                fish_x, fish_y, _ = fish.get_center(got_fish)
                print(fish_x, fish_y, time_fish-time_fish_prev)
                pydirectinput.click(fish_x, fish_y)"""

        else:
            sleep(1)
            send_key(hwnd, '1')
            sleep(0.5)
            send_key(hwnd, 'space')
            sleep(3.5)
            print('no image')


        #cv.imshow('Raw', screenshot)
        
        # debug the loop rate

        


        # press 'q' with the qoutput window focused to exit.
        # waits 1 ms every loop to process key presses

        key = cv.waitKey(1)
        if key == ord('q'):
            cv.destroyAllWindows()
            break

    print('Done.')
    
if __name__ == '__main__':
     main()