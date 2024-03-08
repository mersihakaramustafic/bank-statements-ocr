import cv2
import numpy as np
from pdf2image import convert_from_path
import matplotlib.pyplot as plt
import pytesseract
import re
import constants as c

def convert_pdf(file_path):
    return convert_from_path(file_path, fmt='jpg')[0]

def extract_order_number(thresh):
    # extract purpose of remittance data within particular range
    cropped_image = thresh[c.order_number['start_y'] : c.order_number['end_y'], c.order_number['start_x'] : c.order_number['end_x']]
    extracted_text = pytesseract.image_to_string(cropped_image, config='--oem 3 --psm 4')
    print(extracted_text)

def extract_sender_data(thresh):
    # extract sender's data within particular range
    cropped_image = thresh[820:1070, 160:1720]
    extracted_text = pytesseract.image_to_string(cropped_image)
    print(extracted_text)

def extract_receiver_data(thresh):
    # extract receiver's data within particular range
    cropped_image = thresh[1630:1900, 160:1720]
    extracted_text = pytesseract.image_to_string(cropped_image)
    print(extracted_text)

def extract_purpose_of_remittance_data(thresh):
    # extract purpose of remittance data within particular range
    cropped_image = thresh[1240:1470, 160:1720]
    extracted_text = pytesseract.image_to_string(cropped_image)
    print(extracted_text)

def extract_sender_bank_account(thresh):
    # extract purpose of remittance data within particular range
    cropped_image = thresh[750:830, 2360:3040]
    extracted_text = pytesseract.image_to_string(cropped_image)
    print(extracted_text)

def extract_receiver_bank_account(thresh):
    # extract purpose of remittance data within particular range
    cropped_image = thresh[910:990, 2360:3040]
    extracted_text = pytesseract.image_to_string(cropped_image)
    print(extracted_text)

def extract_amount(thresh):
    # extract purpose of remittance data within particular range
    cropped_image = thresh[1180:1270, 2350:3100]
    extracted_text = pytesseract.image_to_string(cropped_image, config='--oem 3 --psm 4')
    amountRegex = r'\b\d{2}\,\d{2}\b'    
    print(re.findall(amountRegex, extracted_text)[0])

def extract_payment_date(thresh):
    # extract purpose of remittance data within particular range
    cropped_image = thresh[2120:2200, 620:940]
    extracted_text = pytesseract.image_to_string(cropped_image, config='--oem 3 --psm 4')
    print(extracted_text)

file_path = 'C:/Users/PcCentar/Desktop/repos/bank_statements_ocr/bank_statements/report.pdf'
image = convert_pdf(file_path)
image = np.array(image)

# PREPROCESSING

# Resize the image to improve OCR accuracy and speed
image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur to reduce noise and improve accuracy
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

extractedText = pytesseract.image_to_string(thresh, config='--oem 3 --psm 4')
orderNumber = extract_order_number(thresh)
extract_sender_data(thresh)
extract_receiver_data(thresh)
extract_purpose_of_remittance_data(thresh)
extract_sender_bank_account(thresh)
extract_receiver_bank_account(thresh)
extract_amount(thresh)
extract_payment_date(thresh)