import numpy as np
from PIL import Image
import pytesseract
import cv2
import matplotlib.pyplot as plt


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

img = Image.open('test_image.jpg')
img_np = np.array(img)

x_start, y_start, width, height = 200, 450, 800, 2400
cropped_img = img_np[y_start:y_start + height, x_start:x_start + width]

gray_img = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)

custom_config = r'--oem 3 --psm 6'
text = pytesseract.image_to_string(gray_img, config=custom_config, lang='kor')

print("OCR Result:")
print(text)


#---------------------------
plt.figure(figsize=(12, 10))

plt.subplot(1, 3, 1)
plt.title('Original Image')
plt.imshow(img_np)
plt.axis('off')

plt.subplot(1, 3, 2)
plt.title('Cropped Image')
plt.imshow(cropped_img)
plt.axis('off')

plt.subplot(1, 3, 3)
plt.title('Morphed Image')
plt.imshow(gray_img)
plt.axis('off')

plt.tight_layout()
plt.show()