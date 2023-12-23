import time

import pyautogui

x, y = pyautogui.size()  # 保存屏幕尺寸

while True:
    time.sleep(1)
    print(pyautogui.position())

# # 绝对位置移动，移动至屏幕正中心，鼠标移动过渡时间duration设为1秒
# pyautogui.moveTo(x / 2, y / 2, duration=1)
#
# # 相对位置移动，向右100、向上200，鼠标移动过渡时间duration设为0.5秒
# pyautogui.moveRel(100, -200, duration=0.5)
#
# # 移动至屏幕中心点击一下左键，过渡时间0.5秒
# pyautogui.click(x / 2, x / 2, duration=0.5)
#
# # 不指定x、y，在当前位置点击一下右键
# pyautogui.click(button='right')
#
# # 移动至(100,100)点击3次左键，点击间隔0.1s，鼠标移动过渡时间0.5秒
# pyautogui.click(100, 100, clicks=3, interval=0.1, duration=0.5)
#
# # 移动至(100,100)点击2次右键，点击间隔0.5s，鼠标移动过渡时间0.2秒
# pyautogui.click(100, 100, clicks=2, interval=0.5, button=' right', duration=0.2)