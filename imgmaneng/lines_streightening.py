import cv2
import numpy as np

from imgmaneng.img_analyze import img_analyze
from imgmaneng.recognize_letters import recognize_letters
from models.image import Image


def is_not_a_sign(letter):
    if "value" not in letter:
        return True
    c = letter["value"]
    return c != ',' and c != '.' and c != '-' and c != ';' and c != chr(
        34) and c != '*' and c != '+' and c != '_' and c != ':'


def lines_streigtening(img: Image):
    if img.page_info == None:
        img_analyze(img)
        recognize_letters(img)

    final = cv2.imread(img.path).copy()
    for line in img.page_info.text_lines:
        # print(line["uppers"])
        for word in line["words"]:
            offsets = []
            the_biggest = 0
            print(word, end=" ")
            for letter in word["letters"]:
                if letter["h"] > the_biggest:
                    the_biggest = letter["h"]
            for letter in word["letters"]:
                if letter["h"] > ((the_biggest) * 0.6) and letter["y"] > line["uppers"] and is_not_a_sign(
                        letter):  # consider adding statistic test
                    print(letter["h"], ((the_biggest) / 2), letter["y"], line["uppers"])
                    offsets.append(letter["y"] - line["uppers"])
            if (len(offsets) == 0):
                continue
            # print(offsets)
            offset_f = np.mean(offsets)
            offset = int(offset_f)
            print(offset)
            x, y, w, h = word["x"], word["y"], word["w"], word["h"]
            w = w + x
            h = y + h + offset
            print(word)
            roi = final[y:h, x:w]
            print(roi.shape, w, y, h)
            final[(y - offset):(h - offset), x:w] = roi
    return final
