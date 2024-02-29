import cv2
import numpy as np
from pdf2image import convert_from_path
import matplotlib.pyplot as plt
import pytesseract

def convert_pdf(file_path):
    pil_image = convert_from_path(file_path, fmt='jpg')
    return pil_image[0]

file_path = 'C:/Users/PcCentar/Desktop/repos/bank_statements_ocr/bank_statements/report.pdf'

image = convert_pdf(file_path)
plt.imshow(image)
plt.show()
# convert image to numpy array, so it's ready for preprocessing
image = np.array(image)

# PREPROCESSING

# Resize the image to improve OCR accuracy and speed
# You can adjust the size based on your requirements
image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
plt.imshow(image)
plt.show()

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
plt.imshow(gray)
plt.show()

# Apply Gaussian blur to reduce noise and improve accuracy
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
plt.imshow(blurred)
plt.show()

thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
plt.imshow(thresh)
plt.show()

extracted_text = pytesseract.image_to_string(thresh)

print(extracted_text)