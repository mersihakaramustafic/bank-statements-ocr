import cv2
import numpy as np
from pdf2image import convert_from_path
import matplotlib.pyplot as plt
import pytesseract
import re

def convert_pdf(file_path):
    return convert_from_path(file_path, fmt='jpg')[0]

def extract_order_number(text):
    orderNumberRegex = r'\bDPY\d{15}\b'
    
    return re.findall(orderNumberRegex, text)

def extract_amount(text):
    amountRegex = r'\b\d{2}\,\d{2}\b'
    
    return re.findall(amountRegex, text)

def extract_payment_date(text):
    dateRegex = r'\b\d{2}\/\d{2}\/\d{4}\b'

    return re.findall(dateRegex, text)

def extract_sender_data(thresh):
    details = pytesseract.image_to_data(thresh, output_type=pytesseract.Output.DICT, config='--oem 3 --psm 4')

    # extract sender's data within particular range

    cropped_image = image[820:1070, 160:1720]
    # Perform OCR on the extracted region using pytesseract
    extracted_text = pytesseract.image_to_string(cropped_image)
    print(extracted_text)


file_path = 'C:/Users/PcCentar/Desktop/repos/bank_statements_ocr/bank_statements/report.pdf'

image = convert_pdf(file_path)
#plt.imshow(image)
#plt.show()
# convert image to numpy array, so it's ready for preprocessing
image = np.array(image)

# PREPROCESSING

# Resize the image to improve OCR accuracy and speed
image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur to reduce noise and improve accuracy
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
plt.imshow(image)
plt.show()

extractedText = pytesseract.image_to_string(thresh, config='--oem 3 --psm 4')
orderNumber = extract_order_number(extractedText)
amount = extract_amount(extractedText)
paymentDate = extract_payment_date(extractedText)
sender_data = extract_sender_data(thresh)


#print(extractedText)
print(orderNumber)
print(amount)
print(paymentDate)
#print(sender_data)