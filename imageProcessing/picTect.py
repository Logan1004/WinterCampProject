import zxing
import cv2 as cv
import numpy as np
import math

#
# textimage = cv2.imread("1.jpg")
# img0 = cv2.cvtColor(textimage,cv2.COLOR_BGR2GRAY)
# img1 = cv2.equalizeHist(img0)
# cv2.imwrite("img1.png",img1)
#
# img = img1
# h, w = img.shape[:2]
# img = cv2.resize(img, (h*2, w*2), None, 0, 0, cv2.INTER_LINEAR)
# cv2.imwrite("img3.png",img)

def custom_blur_demo(image):
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], np.float32) #锐化
    dst = cv.filter2D(image, -1, kernel=kernel)
    cv.imshow("custom_blur_demo", dst)

def rotate_about_center(src, angle, scale=1.):
    w = src.shape[1]
    h = src.shape[0]
    rangle = np.deg2rad(angle)  # angle in radians
    # now calculate new image width and height
    nw = (abs(np.sin(rangle)*h) + abs(np.cos(rangle)*w))*scale
    nh = (abs(np.cos(rangle)*h) + abs(np.sin(rangle)*w))*scale
    # ask OpenCV for the rotation matrix
    rot_mat = cv.getRotationMatrix2D((nw*0.5, nh*0.5), angle, scale)
    # calculate the move from the old center to the new center combined
    # with the rotation
    rot_move = np.dot(rot_mat, np.array([(nw-w)*0.5, (nh-h)*0.5,0]))
    # the move only affects the translation, so update the translation
    # part of the transform
    rot_mat[0,2] += rot_move[0]
    rot_mat[1,2] += rot_move[1]
    return cv.warpAffine(src, rot_mat, (int(math.ceil(nw)), int(math.ceil(nh))), flags=cv.INTER_LANCZOS4)



textimage = cv.imread("try2.jpg")
textimage = rotate_about_center(textimage,90,1)
custom_blur_demo(textimage)
h, w = textimage.shape[:2]
img = cv.resize(textimage, (h, w*2), None, 0, 0, cv.INTER_LINEAR)
cv.imwrite("ghj.jpg",textimage)

textimage = cv.imread("try2.jpg")
reader = zxing.BarCodeReader()
barcode = reader.decode(textimage)
print(barcode.parsed)
