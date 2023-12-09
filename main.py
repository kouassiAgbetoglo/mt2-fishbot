import GetWindowList



windowName = "Calculatrice"
windowList = GetWindowList.hwnd_window_list(windowName)

hwnd1 = windowList[0]['hwnd']

windowSize = GetWindowList.get_window_size(hwnd1)

print(windowSize)