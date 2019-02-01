import cv2
import numpy as np


def contrast_brightness_image(src1, a, g):
    h, w, ch = src1.shape  # 获取shape的数值，height和width、通道

    # 新建全零图片数组src2,将height和width，类型设置为原图片的通道类型(色素全为零，输出为全黑图片)
    src2 = np.zeros([h, w, ch], src1.dtype)
    dst = cv2.addWeighted(src1, a, src2, 1 - a, g)  # addWeighted函数说明如下
    return dst


capture = cv2.VideoCapture(0)
# capture = cv2.VideoCapture(1) 外接摄像头
ff,ret = capture.read()
ret  = cv2.imread("OldMan.png")

img0 = cv2.cvtColor(ret,cv2.COLOR_BGR2GRAY)
cv2.imwrite("img0.png",img0)



ret = cv2.imread("demo.jpg")
cv2.imwrite("1.jpg", ret)
dst = contrast_brightness_image(ret, 1.5, 10)
cv2.imwrite("2.jpg", dst)
dst = cv2.fastNlMeansDenoisingColored(dst,None,10,10,7,21)

sp = ret.shape
height = sp[0]  # height(rows) of image
width = sp[1]  # width(colums) of image

print(height)
img1 = dst[0:height,0:int(width/3)]
img2 = dst[0:height,int(width/3):int(width*2/3)]
img3 = dst[0:height,int(width*2/3):width-1]
cv2.imwrite("1.jpg", img1)
cv2.imwrite("2.jpg", img2)
cv2.imwrite("3.jpg", img3)
