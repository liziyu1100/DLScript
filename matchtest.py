import cv2

from matplotlib import pyplot as plt

img1 = cv2.imread('./img/main.png')
# 将图片转换为灰度图
img = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

template1 = cv2.imread('./img/template.png')

template = cv2.cvtColor(template1, cv2.COLOR_BGR2GRAY)

th, tw = template.shape[::]
rv = cv2.matchTemplate(img, template, cv2.TM_SQDIFF)

minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(rv)
topLeft = minLoc
bottomRight = (topLeft[0] + tw, topLeft[1] + th)
cv2.rectangle(img, topLeft, bottomRight, 255, 2)
plt.subplot(121), plt.imshow(rv, cmap='gray')
plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(img, cmap='gray')
plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
plt.show()
