from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import cv2

def contrast_brightness_image(src1, a, g):
    h, w, ch = src1.shape  # 获取shape的数值，height和width、通道

    # 新建全零图片数组src2,将height和width，类型设置为原图片的通道类型(色素全为零，输出为全黑图片)
    src2 = np.zeros([h, w, ch], src1.dtype)
    dst = cv2.addWeighted(src1, a, src2, 1 - a, g)  # addWeighted函数说明如下
    return dst

ret=cv2.imread("pic.jpg")
dst = contrast_brightness_image(ret, 1.5, 10)
cv2.imwrite("books_lighten.jpg", dst)
#增亮
dst = cv2.fastNlMeansDenoisingColored(dst,None,10,10,7,21)
#降噪

image=Image.open('books_lighten.jpg').convert('L')
image=np.array(image)
rows,cols=image.shape

iSharp=image
flag1=1
flag2=1
for i in range(rows-1):
        for j in range(cols-1):
            if flag2 == 0:
                x = abs(int(image[i,j+1])-int(image[i,j]))
                y = abs(int(image[i+1,j])-int(image[i,j]))                
            else:
                x = abs(int(image[i+1,j+1])-int(image[i,j]))
                y = abs(int(image[i+1,j])-int(image[i,j+1]))               
            if flag1 == 0:
                iSharp[i,j] = max(x,y)
            else:
                iSharp[i,j] = x+y   
#边缘识别

image0=Image.open('pic.jpg')
image0.show()
image1=Image.open('pic.jpg')
image1.show()
image2 = Image.fromarray(iSharp)
image2.show()
image2.save("edge_detection.jpg")