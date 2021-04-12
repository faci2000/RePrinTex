import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
import cv2


def get_lines_mask(image):
    mask = np.ones(image.shape[:2], dtype=np.uint8)*255
    image_bw = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, image_bw = cv2.threshold(image_bw, 105, 255, cv2.THRESH_BINARY)            # TODO: dependable
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 10))
    image_bw = cv2.morphologyEx(image_bw, cv2.MORPH_OPEN, kernel, iterations=3)

    contours, _ = cv2.findContours(image_bw, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        if 2 * w * h < image.shape[0] * image.shape[1]:
            cv2.rectangle(mask, (x,y), (x+w, y+h), (0, 0, 0), -1)

    return mask


def remove_stains(input_img, x, y):
    image = cv2.imread(input_img.path)
    x_min = np.maximum(0, int(x)-70)        # TODO: dependable
    y_min = np.maximum(0, int(y)-70)
    x_max = np.minimum(image.shape[1], int(x) + 70)
    y_max = np.minimum(image.shape[0], int(y) + 70)

    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    cv2.rectangle(mask, (x_min, y_min), (x_max, y_max), (255, 255, 255), -1)

    cleaned = cv2.inpaint(image, mask, 20, cv2.INPAINT_TELEA)
    return cleaned


def clean_page(input_img):
    lines = input_img.page_info.text_lines
    image = cv2.imread(input_img.path)

    blur = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(blur, (21, 21), 0)
    blur[blur < 200] = 200                          # TODO: dependable
    blur = cv2.cvtColor(blur, cv2.COLOR_GRAY2BGR)

    # mask = np.ones(image.shape[:2], dtype=np.uint8)*255

    # for line in lines:
    #     words = line['words']
    #     for word in words:
    #         cv2.rectangle(mask, (word['x'], word['y']), (word['x']+word['w'], word['y']+word['h']), (0, 0, 0), -1)
    mask = get_lines_mask(image)
    boolean_mask = mask == 255
    cleaned = image.copy()
    cleaned[boolean_mask] = blur[boolean_mask]

    return cleaned


def clean_margins(image):
    image_bw = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_blur = image_bw
    image_bw = get_text_mask(image_bw)

    image_blur[image_blur < 200] = 200                          # TODO: dependable
    image_blur = cv2.cvtColor(image_blur, cv2.COLOR_GRAY2BGR)

    mask = image_bw == 255

    combined = image.copy()
    combined[mask] = image_blur[mask]

    return combined


def get_text_mask(image):
    image_bw = np.ones(image.shape, dtype=np.uint8) * 255
    contours = get_contours(image)

    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        a = cv2.contourArea(c)
        if a > 35000:                                                           # TODO: dependable
            cv2.rectangle(image_bw, (x, y), (x + w, y + h), (0, 0, 0), -1)

    return image_bw


def get_contours(image):
    _, thresh = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV)
    dil = cv2.dilate(thresh, (120, 120), iterations=1)
    contours, _ = cv2.findContours(dil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    return contours


def get_bounding_box(image):
    contours = get_contours(image)
    x_bound, y_bound, w_bound, h_bound = None, None, None, None

    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        if not x_bound or (w_bound <= w and h_bound <= h):
            x_bound, y_bound, w_bound, h_bound = x, y, w, h

    return x_bound, x_bound + w_bound, y_bound, y_bound + h_bound


def increase_contrast(input_img, value=1.7):
    image = cv2.imread(input_img.path)
    image_pil = Image.fromarray(image)
    image_pil = image_pil.filter(ImageFilter.MedianFilter())

    enhancer = ImageEnhance.Contrast(image_pil)
    image_enhanced = enhancer.enhance(value)                    # TODO: dependable
    image_finished = np.asarray(image_enhanced)

    return image_finished

