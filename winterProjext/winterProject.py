from flask import Flask, render_template, redirect, request, url_for , send_file
import os
import zxing
import cv2
import numpy as np
from PIL import Image
import math


app = Flask(__name__, static_url_path='')

@app.route('/')
def hello_world():
    print("helloworld")
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')


def rotate_about_center(src, angle, scale=1.):
    w = src.shape[1]
    h = src.shape[0]
    rangle = np.deg2rad(angle)  # angle in radians
    # now calculate new image width and height
    nw = (abs(np.sin(rangle)*h) + abs(np.cos(rangle)*w))*scale
    nh = (abs(np.cos(rangle)*h) + abs(np.sin(rangle)*w))*scale
    # ask OpenCV for the rotation matrix
    rot_mat = cv2.getRotationMatrix2D((nw*0.5, nh*0.5), angle, scale)
    # calculate the move from the old center to the new center combined
    # with the rotation
    rot_move = np.dot(rot_mat, np.array([(nw-w)*0.5, (nh-h)*0.5,0]))
    # the move only affects the translation, so update the translation
    # part of the transform
    rot_mat[0,2] += rot_move[0]
    rot_mat[1,2] += rot_move[1]
    return cv2.warpAffine(src, rot_mat, (int(math.ceil(nw)), int(math.ceil(nh))), flags=cv2.INTER_LANCZOS4)

@app.route('/search',methods=['POST'])
def search():
    name=request.form["searchbox"]
    capture = cv2.VideoCapture(0)
    # capture = cv2.VideoCapture(1) 外接摄像头
    ff, ret = capture.read()
    h, w, ch = ret.shape  # 获取shape的数值，height和width、通道

    # 新建全零图片数组src2,将height和width，类型设置为原图片的通道类型(色素全为零，输出为全黑图片)
    a=1.5
    g=10
    src2 = np.zeros([h, w, ch], ret.dtype)
    dst = cv2.addWeighted(ret, a, src2, 1 - a, g)  # addWeighted函数说明如下
    dst = cv2.fastNlMeansDenoisingColored(dst, None, 10, 10, 7, 21)
    sp = ret.shape
    height = sp[0]  # height(rows) of image
    width = sp[1]  # width(colums) of image
    print(height)
    img1 = dst[0:height, 0:int(width / 3)]
    img2 = dst[0:height, int(width / 3):int(width * 2 / 3)]
    img3 = dst[0:height, int(width * 2 / 3):width - 1]
    img1 = rotate_about_center(img1,90,1)
    img2 = rotate_about_center(img2,90,1)
    img3 = rotate_about_center(img3,90,1)
    # cv2.imwrite("1.jpg", img1)
    # cv2.imwrite("2.jpg", img2)
    # cv2.imwrite("3.jpg", img3)
    flag = True
    try:
        regImage1 = "1.jpg"
        barcode1 = zxing.BarCodeReader().decode(regImage1)
        print(barcode1.parsed)
        if (barcode1.parsed == '9780684801223' and name == 'The Old Man And The Sea'):
            print( 'The Old Man And The Sea')
            os.system("python3 low_level_right.py")
        else:
            regImage2 = "2.jpg"
            barcode2 = zxing.BarCodeReader().decode(regImage2)
            print(barcode2.parsed)
            if (barcode2.parsed == '9787512508712' and name == 'Othello'):
                print( 'Othello')
                os.system("python3 low_level_left.py")
                flag = True
            else:
                flag = False
    except:
        flag = False

    if (flag==False and name == "宴山亭"):
        flag=True
        os.system("python3 low_level.py")
        #识别

    # print(name)
    # start()
    # os.system("python3 low_level.py")
    if (flag == False):
        return render_template('404.html')
    return render_template('index.html')



if __name__ == '__main__':
    # start()
    # low_level.start()
    app.run()


