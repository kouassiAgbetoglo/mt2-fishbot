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



class PlayGame():
    game_counter = 0
    max_counter = 0
    hwnd = 0

    def __init__(self, needle_img_path):
        self.needle = Vision(needle_img_path)

    def startGame(self, hwnd):
        win32gui.SetForegroundWindow(hwnd)
        sleep(1)
        

    @staticmethod
    def send_key(key=None):
        if key:
            pydirectinput.keyDown(key)
            pydirectinput.keyUp(key)

    @staticmethod
    def left_click(pos):
        x, y = pos
        pydirectinput.click(x, y)

    def use_bait(self):
        self.send_key('1')
        sleep(0.5)
        self.send_key('space')
        sleep(2)
