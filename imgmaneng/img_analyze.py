from numpy.lib.function_base import median
from models.page_info import PageInfo
import cv2
from matplotlib import lines
import numpy as np
import matplotlib.pyplot as plt
import pytesseract
from PIL import Image

def img_analyze(input_img):

    input_img.page_info = PageInfo()
    # read image
    img = cv2.imread(input_img.path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    result_image = img.copy()

    # create sharp negative
    blur = cv2.GaussianBlur(gray,(13,13),0)

    cv2.imwrite("blur.png", blur)
    th, threshed = cv2.threshold(blur, 127, 255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    cv2.imwrite("treshed.png", threshed)

    contours, hierarchy = cv2.findContours(threshed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    #median_letter_width = np.median([contuor[2] for contuor in contours ])
    #median_letter_height = np.median([contuor[3] for contuor in contours ])


    ## get boundaries of whole block of text
    kernel = np.ones((100,100),np.uint8)
    dilation = cv2.dilate(threshed, kernel, iterations = 1)

    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    text_block_x,text_block_y,text_block_w,  text_block_h =  -1,-1,-1,-1

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if text_block_x == -1:
            text_block_x,text_block_y,text_block_w,  text_block_h = x, y, w, h
        if text_block_w<=w and text_block_h<=h:
            text_block_x,text_block_y,text_block_w,  text_block_h = x, y, w, h

    cv2.rectangle(result_image, (text_block_x, text_block_y), (text_block_x + text_block_w, text_block_y + text_block_h), (255, 0, 0), 2)
    
    ## get boundaries of words
    kernel = np.ones((20,50),np.uint8)
    dilation = cv2.dilate(threshed, kernel, iterations = 1)

    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

    words=[]
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if contains(text_block_x,text_block_y,text_block_w,text_block_h,x,y,w,h):
            word={}
            word["x"],word["y"],word["w"],word["h"],word["letters"]=x,y,w,h,[]
            words.append(word)
            cv2.rectangle(result_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    
    ## get boundaries of characters
    kernel = np.ones((7,7),np.uint8)
    dilation = cv2.dilate(threshed, kernel, iterations = 1)
    cv2.imwrite("dilation.png", dilation)

    #preparing data set with letters

    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if contains(text_block_x,text_block_y,text_block_w,text_block_h,x,y,w,h):
            for word in words:
                if contains(word["x"],word["y"],word["w"],word["h"],x,y,w,h):
                    letter={}
                    letter["x"],letter["y"],letter["w"],letter["h"]=x,y,w,h
                    word["letters"].append(letter)
            cv2.rectangle(result_image, (x, y), (x + w, y + h), (0, 0, 255), 2)


    #cv2.imwrite("conturs.png", result_image)

    
    hist = np.mean(threshed,axis=1)
    print(hist)
    #plt.plot(hist)
    

    th_strict = np.mean(threshed)
    th_lose = np.min(hist)*2
    print(th_strict)
    print(th_lose)
    #plt.show()
    H,W = img.shape[:2]
    input_img.page_info.lines["upuppers"] = [y for y in range(text_block_y,text_block_y+text_block_h,1) if hist[y]<=th_lose and hist[y+1]>th_lose]
    input_img.page_info.lines["lolowers"] = [y for y in range(text_block_y,text_block_y+text_block_h,1) if hist[y]>th_lose and hist[y+1]<=th_lose]
    input_img.page_info.lines["uppers"] = [y for y in range(text_block_y,text_block_y+text_block_h,1) if hist[y]<=th_strict and hist[y+1]>th_strict]
    input_img.page_info.lines["lowers"] = [y for y in range(text_block_y,text_block_y+text_block_h,1) if hist[y]>th_strict and hist[y+1]<=th_strict]

    for y in input_img.page_info.lines["upuppers"]:
        cv2.line(result_image, (0,y), (W, y), (0,0,0), 1)

    for y in input_img.page_info.lines["lolowers"]:
        cv2.line(result_image, (0,y), (W, y), (0,250,250), 1)

    for y in input_img.page_info.lines["uppers"]:
        cv2.line(result_image, (0,y), (W, y), (0,0,0), 3)

    for y in input_img.page_info.lines["lowers"]:
        cv2.line(result_image, (0,y), (W, y), (0,250,250), 3)

    cv2.imwrite("result.png", result_image)
    fill_lines(input_img,words,input_img.page_info.lines["uppers"],input_img.page_info.lines["lowers"])
    #final=move_letters(text_lines,img)

    #cv2.imwrite("final.png", final)

    

def found_proper_line(uppers,lowers,word):
    i=0
    #print(len(uppers),i ,uppers[i],(word["y"]+word["h"]),(uppers[i]>(word["y"]+word["h"])) ,lowers[i],word["y"],(lowers[i]<word["y"]))
    while(len(uppers)>i and ((uppers[i]>(word["y"]+word["h"])) or (lowers[i]<word["y"]))):
        #print(uppers[i],(word["y"]+word["h"]),lowers[i],word["y"])
        i+=1
    #print(i)
    if (i==len(uppers)):
        return -1
    return i


def fill_lines(input_image,words,uppers,lowers):
    input_image.page_info.text_lines=[{"uppers":uppers[i],"words":[]} for i in range(len(uppers))]
    for word in words:
        i=found_proper_line(uppers,lowers,word)
        #print(uppers[i],word["y"])
        if i!=-1:
            input_image.page_info.text_lines[i]["words"].append(word)


# def move_letters(text_lines,img):
#     final = img.copy()
#     for line in text_lines:
#         print(line["uppers"])
#         for word in line["words"]:
#             offsets=[]
#             the_biggest=0
#             print(word)
#             for letter in word["letters"]:
#                 if letter["h"]>the_biggest:
#                     the_biggest=letter["h"]
#             for letter in word["letters"]:
               
#                 if letter["h"]>((the_biggest)/2) and letter["y"]>line["uppers"]: 
#                     print(letter["h"],((the_biggest)/2),letter["y"],line["uppers"])
#                     offsets.append(letter["y"]-line["uppers"])
#             if(len(offsets)==0):
#                 continue
#             print(offsets)
#             offset_f=np.mean(offsets)
#             offset=int(offset_f)
#             print(offset)
#             x,y,w,h=word["x"],word["y"],word["w"],word["h"]
#             w=w+x
#             h=y+h
#             print(word)
#             roi=img[y:h,x:w]
#             print(roi.shape,w,y,h)
#             final[(y-offset):(h-offset),x:w]=roi
#     return final

            
def contains(big_x,big_y,big_w,big_h,s_x,s_y,s_w,s_h):
    return big_x<=s_x and big_y<=s_y and (big_x+big_w)>=(s_x+s_w) and (big_y+big_h)>=(s_y+s_h)





#find_lines("test.jpg")
