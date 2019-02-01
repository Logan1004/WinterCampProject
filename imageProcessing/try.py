
#coding=utf-8
import cv2
import  numpy as np
'''双线性插值'''
textimage = cv2.imread("1.jpg")
img = cv2.cvtColor(textimage,cv2.COLOR_BGR2GRAY)
cv2.imwrite('img.jpg', img)
h, w = img.shape[:2]

# shrink to half of the original
a1 = np.array([[0.5, 0, 0], [0, 0.5, 0]], np.float32)
d1 = cv2.warpAffine(img, a1, (w, h), borderValue=125)

# shrink to half of the original and move
a2 = np.array([[0.5, 0, w /4], [0, 0.5, h / 4]], np.float32)
d2 = cv2.warpAffine(img, a2, (w, h),flags=cv2.INTER_NEAREST,borderValue=125)
# rotate based on d2
a3 = cv2.getRotationMatrix2D((w / 2, h / 2), 90, 1)
d3 = cv2.warpAffine(d2, a3, (w, h),flags=cv2.INTER_LINEAR, borderValue=125)

# cv2.imshow('img',img)
# cv2.imshow('d1',d1)
# cv2.imshow('d2',d2)
# cv2.imshow('d3',d3)
# cv2.waitKey(0)


cv2.imwrite("try0.jpg",img)
cv2.imwrite("try1.jpg",d1)
cv2.imwrite("try2.jpg",d2)
cv2.imwrite("try3.jpg",d3)



cv2.destroyAllWindows()

