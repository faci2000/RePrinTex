from PyQt5 import QtGui
import numpy as np

def convert_QImage_to_cv2Image(in_img:QtGui.QImage):
    in_img = in_img.convertToFormat(QtGui.QImage.Format.Format_RGB32)
    
    width = in_img.width()
    height = in_img.height()

    ptr = in_img.constBits()
    arr = np.array(ptr).reshape(height, width, 4) 
    return arr

def convert_QPixmap_to_QImage(pixmap:QtGui.QPixmap)->QtGui.QImage:
    return pixmap.toImage()

def convert_QPixmap_to_cv2Image(in_img:QtGui.QImage):
    return convert_QImage_to_cv2Image(convert_QPixmap_to_QImage(in_img))