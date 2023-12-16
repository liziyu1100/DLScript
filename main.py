import cv2
import numpy as np

# 读取图片，丢弃Alpha通道，转为灰度图
a = cv2.imread('pc_activity_btn.png', cv2.IMREAD_GRAYSCALE)
# 读取图片，并保留Alpha通道
b = cv2.imread('transparent_activity_btn.png', cv2.IMREAD_UNCHANGED)

# 取出Alpha通道
alpha = b[:,:,3]
b = cv2.cvtColor(b, cv2.COLOR_BGRA2GRAY)
cv2.imshow("test", b)
# 模板匹配，将alpha作为mask，TM_CCORR_NORMED方法的计算结果范围为[0, 1]，越接近1越匹配
result = cv2.matchTemplate(a, b, cv2.TM_SQDIFF)
# 获取结果中最大值和最小值以及他们的坐标
print(cv2.minMaxLoc(result))
cv2.waitKey()
# 运行结果：
# (0.9999997615814209, 0.9999997615814209, (0, 0), (0, 0))