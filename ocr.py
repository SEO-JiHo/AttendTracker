import numpy as np
from PIL import Image
import pytesseract
import cv2
# import matplotlib.pyplot as plt

def process_ocr(image):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    img = Image.open(image)
    img_np = np.array(img)

    x_start, y_start, width, height = 200, 450, 800, 2400
    cropped_img = img_np[y_start:y_start + height, x_start:x_start + width]

    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(cropped_img, config=custom_config, lang='kor')

    return text

#-----------------------------
# plt.figure(figsize=(12, 10))
#
# plt.subplot(1, 3, 1)
# plt.title('Original Image')
# plt.imshow(img_np)
# plt.axis('off')
#
# plt.subplot(1, 3, 2)
# plt.title('Cropped Image')
# plt.imshow(cropped_img)
# plt.axis('off')
#
# plt.subplot(1, 3, 3)
# plt.title('gray Image')
# plt.imshow(gray_img)
# plt.axis('off')
#
# plt.tight_layout()
# plt.show()