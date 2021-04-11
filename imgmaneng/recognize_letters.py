from imgmaneng.img_analyze import img_analyze
from models.image import Image
import pytesseract
import cv2


def recognize_letters(input_image:Image):
    
    if input_image.page_info is None:
        img_analyze(input_image)
    
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

    img = cv2.imread(input_image.path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(13,13),0)
    th, threshed = cv2.threshold(blur, 127, 255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    for line in input_image.page_info.text_lines:
        for word in line["words"]:
            rec_letters = pytesseract.image_to_string(threshed[word["y"]:(word["y"]+word["h"]),word["x"]:(word["x"]+word["w"])],config='--psm 8',lang='pol') # recognize whole word
            print(rec_letters[:len(rec_letters)-2])
            word["letters"].sort(key=lambda letter: letter["x"])
            # for letter in word["letters"]:
            #     rec_letters = pytesseract.image_to_string(threshed[letter["y"]:(letter["y"]+letter["h"]),letter["x"]:(letter["x"]+letter["w"])],config='--psm 10',lang='pol') # recognize whole word
            #     print(rec_letters[:len(rec_letters)-2])
            if len(rec_letters)-2 == len(word["letters"]):
                for i in range(len(word["letters"])):
                    word["letters"][i]["value"]=rec_letters[i]
                    if rec_letters[i] not in input_image.page_info.letters:
                        input_image.page_info.letters[rec_letters[i]]=[]
                    input_image.page_info.letters[rec_letters[i]].append(word["letters"][i])
            #cv2.imshow("word",threshed[word["y"]:(word["y"]+word["h"]),word["x"]:(word["x"]+word["w"])])

    print(input_image.page_info.letters)


