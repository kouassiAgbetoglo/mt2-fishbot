import win32gui, win32ui, win32con
import numpy as np
from threading import Thread,Lock


class WindowCapture():

    stopped = True
    lock = None
    screenshot = None 


    w = 0 # set this
    h = 0 # set this
    hwnd = None
    cropped_x = 0
    cropped_y = 0
    offset_x = 0
    offset_y = 0
    def __init__(self,window_name=None):
        self.lock = Lock()


        if window_name is None:
            self.hwnd = win32gui.GetDesktopWindow()
        else:
            self.hwnd = win32gui.FindWindow(None,window_name)
            if not self.hwnd:
                raise Exception('Window not found: {}'.format(window_name))
        #Get the window size
        window_rect = win32gui.GetWindowRect(self.hwnd)
        self.w= window_rect[2] - window_rect[0]
        self.h=window_rect[3] - window_rect[1]

        #GetOnlyTheGameScreen
        borderpixels=8
        titlebar_pixels=30
        self.w = self.w - (borderpixels*2)
        self.h = self.h - (borderpixels*2)
        self.cropped_x=borderpixels
        self.cropped_y=titlebar_pixels

        #TakesTheRealCoordonate in game
        self.offset_x = window_rect[0]+self.cropped_x
        self.offset_y = window_rect[1]+self.cropped_y


    @staticmethod
    def list_window_name():
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                print(hwnd, win32gui.GetWindowText(hwnd))
        win32gui.EnumWindows(winEnumHandler,None)
    #list_window_name()




    def getscreenshot(self):

        #bmpfilenamename = "out.bmp" #set this

      
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj=win32ui.CreateDCFromHandle(wDC)
        cDC=dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj,self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0,0),(self.w, self.h) , dcObj, (self.cropped_x,self.cropped_y), win32con.SRCCOPY)
    
        #Save the screenshot
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.frombuffer(signedIntsArray, dtype='uint8')
        img.shape = (self.h, self.w, 4)
        

        # Free Resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())
        #Remove transparacy filter
        img = img[...,:3]
        img = np.ascontiguousarray(img)

        return(img)

    def get_screen_position(self,pos):
        return (pos[0]+self.offset_x, pos[1]+self.offset_y)
    
    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()
    def stop(self):
        self.stop = True

    def run(self):
        while not self.stopped:
            screenshot= self.getscreenshot()
            self.lock.acquire()
            self.screenshot=screenshot
            self.lock.release()