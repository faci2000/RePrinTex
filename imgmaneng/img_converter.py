from PyQt5 import QtGui
import cv2
import numpy as np
from PyQt5.QtGui import QImage, QPixmap, qBlue, qGreen, qRed


def convert_QImage_to_cv2Image(in_img:QImage):
    in_img = in_img.convertToFormat(QtGui.QImage.Format.Format_RGB32)
    
    width = in_img.width()
    height = in_img.height()

    ptr = in_img.bits()
    ptr.setsize(height * width * 4)
    arr = np.array(ptr).reshape(height, width, 4)
    return arr

def convert_QPixmap_to_QImage(pixmap:QPixmap)->QImage:
    return pixmap.toImage()

def convert_QPixmap_to_cv2Image(in_img:QImage):
    return convert_QImage_to_cv2Image(convert_QPixmap_to_QImage(in_img))

def convert_cv2Image_to_QPixmap(clean):
    return QPixmap(QImage(clean, clean.shape[1], clean.shape[0], clean.shape[1] * 3, QImage.Format_RGB888))

def QImage2CV(pixmap):
    
    tmp = convert_QPixmap_to_QImage(pixmap)
    
    #Use numpy to create an empty image
    cv_image = np.zeros((tmp.height(), tmp.width(), 3), dtype=np.uint8)
    
    for row in range(0, tmp.height()):
        for col in range(0,tmp.width()):
            r = qRed(tmp.pixel(col, row))
            g = qGreen(tmp.pixel(col, row))
            b = qBlue(tmp.pixel(col, row))
            cv_image[row,col,0] = r
            cv_image[row,col,1] = g
            cv_image[row,col,2] = b
    cv2.imwrite("converted.png", cv_image)
    return cv_image