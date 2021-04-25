from imgmaneng.img_analyze import img_analyze
import cv2
from models.image import Image
from models.effects import Effects
from PyQt5.QtGui import QImage, QPixmap

def draw_lines_and_boundaries(image:Image,effects:Effects)->QPixmap:
    img = cv2.imread(image.path)
    print(image.page_info)
    if image.page_info is None:
        img_analyze(image)

    if effects.text_block:
        print("block")
        cv2.rectangle(img, (image.page_info.text_block["x"], image.page_info.text_block["y"]),
                  (image.page_info.text_block["x"] + image.page_info.text_block["w"], image.page_info.text_block["y"] + image.page_info.text_block["h"]), (255, 0, 0), 2)

    if effects.words:
        print("words")
        for line in image.page_info.text_lines:
            for word in line["words"]:
                cv2.rectangle(img, (word["x"], word["y"]),
                  (word["x"] + word["w"], word["y"] + word["h"]), (0, 255, 0), 2)

    if effects.letters:
        print("letters")
        for line in image.page_info.text_lines:
            for word in line["words"]:
                for letter in word["letters"]:
                    cv2.rectangle(img, (letter["x"], letter["y"]),
                  (letter["x"] + letter["w"], letter["y"] + letter["h"]), (0, 0, 255), 2)
    
    if effects.minor_lines:
        print("minor_lines")
        H, W = img.shape[:2]
        for y in image.page_info.lines["upuppers"]:
            cv2.line(img, (0, y), (W, y), (0, 0, 0), 1)

        for y in image.page_info.lines["lolowers"]:
            cv2.line(img, (0, y), (W, y), (0, 250, 250), 1)
    

    if effects.main_lines:
        print(image.page_info.lines["uppers"])
        H, W = img.shape[:2]
        for y in image.page_info.lines["uppers"]:
            print(y)
            cv2.line(img, (0, y), (W, y), (0, 0, 0), 3)

        for y in image.page_info.lines["lowers"]:
            print(y)
            cv2.line(img, (0, y), (W, y), (0, 250, 250), 3)

    return  QPixmap(QImage(img.data, img.shape[1], img.shape[0], img.shape[1] * 3, QImage.Format_RGB888))