import cv2
import numpy
import numpy as np

from imgmaneng.img_analyze import img_analyze
from models.image import Image


def draw_lines_and_boundaries(image: Image, img: np.ndarray, lines) -> numpy.ndarray:
    from models.effects import Lines
    if image.page_info is None:
        img_analyze(image)

    if Lines.TEXT_BLOCK.value in lines:
        print("block")
        cv2.rectangle(img, (image.page_info.text_block["x"], image.page_info.text_block["y"]),
                      (image.page_info.text_block["x"] + image.page_info.text_block["w"],
                       image.page_info.text_block["y"] + image.page_info.text_block["h"]), (255, 0, 0), 2)

    if Lines.WORDS.value in lines:
        print("words")
        for line in image.page_info.text_lines:
            for word in line["words"]:
                cv2.rectangle(img, (word["x"], word["y"]),
                              (word["x"] + word["w"], word["y"] + word["h"]), (0, 255, 0), 2)

    if Lines.LETTERS.value in lines:
        print("letters")
        for line in image.page_info.text_lines:
            for word in line["words"]:
                for letter in word["letters"]:
                    cv2.rectangle(img, (letter["x"], letter["y"]),
                                  (letter["x"] + letter["w"], letter["y"] + letter["h"]), (0, 0, 255), 2)

    if Lines.MINOR_LINES.value in lines:
        print("minor_lines")
        H, W = img.shape[:2]
        for y in image.page_info.lines["upuppers"]:
            cv2.line(img, (0, y), (W, y), (0, 0, 0), 1)

        for y in image.page_info.lines["lolowers"]:
            cv2.line(img, (0, y), (W, y), (0, 250, 250), 1)

    if Lines.MAIN_LINES.value in lines:
        print("main lines")
        H, W = img.shape[:2]
        for y in image.page_info.lines["uppers"]:
            cv2.line(img, (0, y), (W, y), (0, 0, 0), 3)

        for y in image.page_info.lines["lowers"]:
            cv2.line(img, (0, y), (W, y), (0, 250, 250), 3)

    return img  # QPixmap(QImage(img.data, img.shape[1], img.shape[0], img.shape[1] * 3, QImage.Format_RGB888))
