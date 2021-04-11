import cv2
from matplotlib import lines
import numpy as np
import matplotlib.pyplot as plt
import pytesseract
from PIL import Image

def contains(big_x,big_y,big_w,big_h,s_x,s_y,s_w,s_h):
    return big_x<=s_x and big_y<=s_y and (big_x+big_w)>=(s_x+s_w) and (big_y+big_h)>=(s_y+s_h)

def find_lines(image):

    # read image
    img = cv2.imread(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    result_image = img.copy()


    # create sharp negative
    blur = cv2.GaussianBlur(gray,(13,13),0)

    cv2.imwrite("blur.png", blur)
    th, threshed = cv2.threshold(blur, 127, 255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    cv2.imwrite("treshed.png", threshed)

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
        let_to_rec = Image.fromarray(threshed[y:(y+h),x:(x+w)].astype(np.uint8))
        rec_lett=pytesseract.image_to_string(let_to_rec,config='--psm 8',lang='pol') # recognize the letter
        print(rec_lett)
        cv2.imshow("letter",threshed[y:(y+h),x:(x+w)])
        cv2.waitKey(0)
        if contains(text_block_x,text_block_y,text_block_w,text_block_h,x,y,w,h):
            words.append((x,y,w,h,[]))
            cv2.rectangle(result_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    
    ## get boundaries of characters
    kernel = np.ones((7,7),np.uint8)
    dilation = cv2.dilate(threshed, kernel, iterations = 1)
    cv2.imwrite("dilation.png", dilation)

    #preparing data set with letters
    letters= {}
            # x,y,w,h=word[0],word[1],word[2],word[3]
            # w=w+x
            # h=y+h
            # print(word)
            # roi=img[y:h,x:w]

    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        
        let_to_rec = Image.fromarray(threshed[y:(y+h),x:(x+w)].astype(np.uint8))
        cv2.imshow("letter",threshed[y:(y+h),x:(x+w)])
        cv2.waitKey(0)
        rec_lett=pytesseract.image_to_string(threshed[y:(y+h),x:(x+w)],config='--psm 10',lang='pol') # recognize the letter
        print(rec_lett)
        if rec_lett not in letters:
            letters[rec_lett]=[]
        letters[rec_lett].append((x,y,w,h))

        if contains(text_block_x,text_block_y,text_block_w,text_block_h,x,y,w,h):
            for word in words:
                if contains(word[0],word[1],word[2],word[3],x,y,w,h):
                    word[4].append((x,y,w,h))
            #words.append((x,y,w,h))
            cv2.rectangle(result_image, (x, y), (x + w, y + h), (0, 0, 255), 2)


    cv2.imwrite("conturs.png", result_image)

    
    hist = np.mean(threshed,axis=1)
    print(hist)
    #plt.plot(hist)
    

    th_strict = np.mean(threshed)
    th_lose = np.min(hist)*2
    print(th_strict)
    print(th_lose)
    #plt.show()
    H,W = img.shape[:2]
    upuppers = [y for y in range(text_block_y,text_block_y+text_block_h,1) if hist[y]<=th_lose and hist[y+1]>th_lose]
    lolowers = [y for y in range(text_block_y,text_block_y+text_block_h,1) if hist[y]>th_lose and hist[y+1]<=th_lose]
    uppers = [y for y in range(text_block_y,text_block_y+text_block_h,1) if hist[y]<=th_strict and hist[y+1]>th_strict]
    lowers = [y for y in range(text_block_y,text_block_y+text_block_h,1) if hist[y]>th_strict and hist[y+1]<=th_strict]

    for y in upuppers:
        cv2.line(result_image, (0,y), (W, y), (0,0,0), 1)

    for y in lolowers:
        cv2.line(result_image, (0,y), (W, y), (0,250,250), 1)

    for y in uppers:
        cv2.line(result_image, (0,y), (W, y), (0,0,0), 3)

    for y in lowers:
        cv2.line(result_image, (0,y), (W, y), (0,250,250), 3)

    cv2.imwrite("result.png", result_image)
    text_lines=create_lines(words,uppers,lowers)
    final=move_letters(text_lines,img)

    cv2.imwrite("final.png", final)

    

def found_proper_line(uppers,lowers,word):
    i=0
    print(len(uppers),i ,uppers[i],(word[1]+word[3]),(uppers[i]>(word[1]+word[3])) ,lowers[i],word[1],(lowers[i]<word[1]))
    while(len(uppers)>i and ((uppers[i]>(word[1]+word[3])) or (lowers[i]<word[1]))):
        #print(uppers[i],(word[1]+word[3]),lowers[i],word[1])
        i+=1
    print(i)
    if (i==len(uppers)):
        return -1
    return i


def create_lines(words,uppers,lowers):
    text_lines=[(uppers[i],[]) for i in range(len(uppers))]
    for word in words:
        i=found_proper_line(uppers,lowers,word)
        print(uppers[i],word[1])
        if i!=-1:
            text_lines[i][1].append(word)
    return text_lines


def move_letters(text_lines,img):
    final = img.copy()
    for line in text_lines:
        print(line[0])
        for word in line[1]:
            offsets=[]
            the_biggest=0
            print(word)
            for letter in word[4]:
                if letter[3]>the_biggest:
                    the_biggest=letter[3]
            for letter in word[4]:
               
                if letter[3]>((the_biggest)/2) and letter[1]>line[0]: 
                    print(letter[3],((the_biggest)/2),letter[1],line[0])
                    offsets.append(letter[1]-line[0])
            if(len(offsets)==0):
                continue
            print(offsets)
            offset_f=np.mean(offsets)
            offset=int(offset_f)
            print(offset)
            x,y,w,h=word[0],word[1],word[2],word[3]
            w=w+x
            h=y+h
            print(word)
            roi=img[y:h,x:w]
            print(roi.shape,w,y,h)
            final[(y-offset):(h-offset),x:w]=roi
    return final

            





find_lines("test.jpg")