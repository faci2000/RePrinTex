import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
import cv2


def clean_page(image, upper_shift, lower_shift)->np.ndarray:
    #image = cv2.imread(input_img.path)
    cv2.imwrite("converted.png", image)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    original = gray.copy()

    upper, lower = _get_peaks(gray)
    mask_margin = _get_text_mask(gray)

    mask_upper = upper + upper_shift > gray
    mask_lower = gray < lower + lower_shift
    mask_lower = np.bitwise_and(mask_lower, mask_margin)

    gray[mask_upper] = upper
    gray[mask_lower] = original[mask_lower]

    image_finished = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    return image_finished


def remove_stains(image, x, y, r)->np.ndarray:
    # image = cv2.imread(input_img.path)

    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    cv2.circle(mask, (x, y), r, (255, 255, 255), -1)
    cleaned = cv2.inpaint(image, mask, 20, cv2.INPAINT_TELEA)
    return cleaned


def increase_contrast(input_img, intensity=1.3)->np.ndarray:
    #image = cv2.imread(input_img.path)
    image_pil = Image.fromarray(input_img)

    image_pil = image_pil.filter(ImageFilter.MedianFilter())
    enhancer = ImageEnhance.Contrast(image_pil)
    image_enhanced = enhancer.enhance(intensity)
    image_finished = np.asarray(image_enhanced)
    return image_finished


def _get_text_mask(image):
    image_bw = np.ones(image.shape, dtype=np.uint8)
    contours = _get_block_contours(image)

    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(image_bw, (x, y), (x + w, y + h), (255, 255, 255), -1)

    image_bw = image_bw == 255
    return image_bw


def _get_peaks(image):
    small = _rescale(image, 0.4)
    hist = cv2.calcHist([small], [0], None, [256], [0, 256])
    hist_smooth = cv2.GaussianBlur(hist, (9, 9), 0, 0, cv2.BORDER_REPLICATE)

    peaks = []
    for i, v in enumerate(hist_smooth):
        if i == 0 or i == len(v) - 1:
            continue
        if hist[i - 1][0] < hist[i][0] and hist[i + 1][0] < hist[i][0]:
            peaks.append((i, v[0]))
    peaks = sorted(peaks, key=lambda x: x[1], reverse=True)

    if len(peaks) < 2:
        upper = lower = peaks[0][0]
    else:
        upper = peaks[0][0]
        lower = peaks[1][0]

        i = 0
        while lower > 120:
            lower = peaks[i][0]
            i += 1

    return upper, lower


def _get_block_contours(image):
    _, thresh = cv2.threshold(image, 100, 255, cv2.THRESH_BINARY_INV)
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (100, 10))
    dil = cv2.dilate(thresh, rect_kernel, iterations=1)
    contours, _ = cv2.findContours(dil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    return contours


def _rescale(frame, scale=0.1):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    return cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)
