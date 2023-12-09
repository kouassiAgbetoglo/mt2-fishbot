from ctypes import *
from typing import List, Dict
import win32process, win32gui, win32api, win32con
import pyautogui
import pydirectinput
import win32gui
import time

def send_keys_to_window(hwnd, keys):
    win32gui.SetForegroundWindow(hwnd)
    pydirectinput.press(keys)

def click_to_window(hwnd, x, y):
    win32gui.SetForegroundWindow(hwnd)
    pydirectinput.moveTo(x, y)
    pydirectinput.click()


class WindowHandler:
    

    def hwnd_window_list(self, windowName) -> List[Dict[str, int]]:
        def callback(hwnd, hwnds):
            if not win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
                return
            if win32gui.GetWindowText(hwnd).startswith(windowName) != True:
                return
            window_text = win32gui.GetWindowText(hwnd)
            if window_text.startswith(windowName):
                new_name = "METIN2 - " + str(hwnd)  
                win32gui.SetWindowText(hwnd, new_name)
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            hwnds.append({"pid": pid, "hwnd": hwnd})

        windows = []
        win32gui.EnumWindows(callback, windows)
        return windows


    
    @staticmethod
    def get_window_size(hwnd):
        # window size
        window_rect = win32gui.GetWindowRect(hwnd)
        w = window_rect[2] - window_rect[0]
        h = window_rect[3] - window_rect[1]
        return h, w

    @staticmethod
    def rename_window(hwnd, name):
        win32gui.SetWindowText(hwnd, name)
