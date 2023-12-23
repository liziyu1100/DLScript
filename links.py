import copy
import ctypes
from ctypes.wintypes import RECT, HWND
import numpy as np
import pyautogui
# use 'pip install pywin32' to install
import win32con, win32gui
from PIL import Image, ImageGrab

import time

# 防止UI放大导致截图不完整
# windll.user32.SetProcessDPIAware()

start_pos = []
def get_window_rect(hwnd):
    try:
        f = ctypes.windll.dwmapi.DwmGetWindowAttribute
    except WindowsError:
        f = None
    if f:
        rect = ctypes.wintypes.RECT()
        DWMWA_EXTENDED_FRAME_BOUNDS = 9
        f(ctypes.wintypes.HWND(hwnd),
          ctypes.wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
          ctypes.byref(rect),
          ctypes.sizeof(rect)
          )
        return rect.left, rect.top, rect.right, rect.bottom


def get_window_pos(name):
    name = name
    handle = win32gui.FindWindow(0, name)
    # 获取窗口句柄
    if handle == 0:
        return None
    else:
        # 返回坐标值和handle
        return get_window_rect(handle), handle


def fetch_image():

    (x1, y1, x2, y2), handle = get_window_pos("Yu-Gi-Oh! DUEL LINKS")
    pyautogui.click(x1+50, y1+100, duration=0.2)
    # 发送还原最小化窗口的信息
    win32gui.SendMessage(handle, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
    # 设为高亮
    win32gui.SetForegroundWindow(handle)
    # 截图
    grab_image = ImageGrab.grab((x1, y1, x2, y2))

    return cv2.cvtColor(np.asarray(grab_image),cv2.COLOR_RGB2BGR),[x1,y1]




def click(th, tw, maxLoc):
    topLeft = maxLoc
    # topLeft = minLoc
    pos = [start_pos[0] + topLeft[0] + tw / 2, start_pos[1] + topLeft[1] + th / 2]
    pyautogui.click(pos[0], pos[1], duration=0.2)
def isRight(image, template1):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 读取图片，并保留Alpha通道
    template = cv2.cvtColor(template1, cv2.COLOR_BGR2GRAY)
    th, tw = template.shape[::]
    # 模板匹配，将alpha作为mask，TM_CCORR_NORMED方法的计算结果范围为[0, 1]，越接近1越匹配
    result = cv2.matchTemplate(gray, template, cv2.TM_CCORR_NORMED)
    # result = cv2.matchTemplate(gray, template, cv2.TM_SQDIFF)
    # 获取结果中最大值和最小值以及他们的坐标
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
    if maxVal < 0.9:
        return 0
    else:
        click(th, tw, maxLoc)


if __name__ == "__main__":
    import cv2
    image, start_pos = fetch_image()
    template = cv2.imread('./img/start_game.png', cv2.IMREAD_UNCHANGED)
    template2 = cv2.imread('./img/gate.png', cv2.IMREAD_UNCHANGED)
    template3 = cv2.imread('./img/duel.png', cv2.IMREAD_UNCHANGED)
    template4 = cv2.imread('./img/duel_end.png', cv2.IMREAD_UNCHANGED)
    template5 = cv2.imread('./img/next.png', cv2.IMREAD_UNCHANGED)
    # while True:
    image, start_pos = fetch_image()
    time.sleep(1)
    while True:
        if pyautogui.position().x==0 and pyautogui.position().y==0:
            break;  ##exit程序
        image, start_pos = fetch_image()
        time.sleep(0.3)
        isRight(image, template)
        isRight(image, template2)
        isRight(image, template3)
        isRight(image, template4)
        isRight(image, template5)
        pyautogui.click(start_pos[0]+1034, start_pos[1]+235,duration=0.3)


