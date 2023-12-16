import ctypes
from ctypes.wintypes import RECT, HWND
import numpy as np
import pyautogui
# use 'pip install pywin32' to install
import win32api, win32con, win32gui
from PIL import Image, ImageGrab

import time

# 防止UI放大导致截图不完整
# windll.user32.SetProcessDPIAware()

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


def get_window_pos(win_name):
    handle = win32gui.FindWindow(0, win_name)
    # 获取窗口句柄
    if handle == 0:
        return None
    else:
        # 返回坐标值和handle
        return get_window_rect(handle), handle


def fetch_image(win_name):
    (x1, y1, x2, y2), handle = get_window_pos(win_name)
    # 发送还原最小化窗口的信息
    win32gui.SendMessage(handle, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
    # 设为高亮
    win32gui.SetForegroundWindow(handle)
    # 截图
    grab_image = ImageGrab.grab((x1, y1, x2, y2))

    return cv2.cvtColor(np.asarray(grab_image),cv2.COLOR_RGB2BGR),[x1,y1]


def click(pos):
    pyautogui.click(pos[0], pos[1], duration=0.2)


if __name__ == "__main__":
    import cv2
    name = "Yu-Gi-Oh! DUEL LINKS"
    image, start_pos = fetch_image()
    # 转为灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ih, iw = gray.shape[::]
    # 读取图片，并保留Alpha通道
    template = cv2.imread('pic1.png', cv2.IMREAD_UNCHANGED)
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    th, tw = template.shape[::]
    #模板匹配，将alpha作为mask，TM_CCORR_NORMED方法的计算结果范围为[0, 1]，越接近1越匹配
    result = cv2.matchTemplate(gray, template, cv2.TM_SQDIFF)
    # 获取结果中最大值和最小值以及他们的坐标
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
    topLeft = minLoc
    bottomRight = (topLeft[0] + tw, topLeft[1] + th)
    pos = [start_pos[0] + topLeft[0] + tw/2,start_pos[1] + topLeft[1] + th/2]
    click(pos)
    # 在窗口截图中匹配位置画红色方框
    # cv2.rectangle(image, topLeft, bottomRight, 255, 2)
    # cv2.imshow('Match Template', image)
    # cv2.waitKey()