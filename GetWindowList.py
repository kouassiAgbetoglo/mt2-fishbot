from ctypes import *
from typing import List, Dict
import win32process, win32gui


def hwnd_window_list(windowName) -> List[Dict[str, int]]:
    def callback(hwnd, hwnds):
        if not win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
            return
        if win32gui.GetWindowText(hwnd).startswith(windowName) != True:
            return
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        hwnds.append({"pid": pid, "hwnd": hwnd})

    windows = []
    win32gui.EnumWindows(callback, windows)
    return windows


def get_window_size(hwnd):
    # window size
    window_rect = win32gui.GetWindowRect(hwnd)
    w = window_rect[2] - window_rect[0]
    h = window_rect[3] - window_rect[1]
    return h, w


