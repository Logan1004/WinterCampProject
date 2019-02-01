import cv2
import numpy as np

# def contrast_brightness_image(src1, a, g):
#     h, w, ch = src1.shape  # 获取shape的数值，height和width、通道
#
#     # 新建全零图片数组src2,将height和width，类型设置为原图片的通道类型(色素全为零，输出为全黑图片)
#     src2 = np.zeros([h, w, ch], src1.dtype)
#     dst = cv2.addWeighted(src1, a, src2, 1 - a, g)  # addWeighted函数说明如下
#     return dst
#
# ret = cv2.imread("pic.jpg")
# cv2.imwrite("1.jpg", ret)
# dst = contrast_brightness_image(ret, 1.5, 10)
# cv2.imwrite("2.jpg", dst)
# dst = cv2.fastNlMeansDenoisingColored(dst,None,10,10,7,21)
#
# textimage = cv2.imread("2.jpg")
# img = cv2.cvtColor(textimage,cv2.COLOR_BGR2GRAY)
# cv2.imwrite("3.jpg",img)
#
# ret = cv2.imread("5OldMan.png")
# sp = ret.shape
# height = sp[0]  # height(rows) of image
# width = sp[1]
# img1 = ret[0:int(height/2),0:width]
# img2 = ret[int(height/2)-30:height,0:width]
# cv2.imwrite("4.jpg",img1)
# cv2.imwrite("5.jpg",img2)
#
textimage = cv2.imread("7barcoderotate.jpg")
sp = textimage.shape
h = sp[0]  # height(rows) of image
w = sp[1]

img = cv2.resize(textimage, (h*2, w), None, 0, 0, cv2.INTER_LINEAR)
cv2.imwrite("8.jpg",textimage)