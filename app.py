import cv2
import numpy as np
from pdf2image import convert_from_path
#import matplotlib.pyplot as plt
import pytesseract
import re
import constants as c
import json
from flask import Flask

def convert_pdf(file_path):
    try:
        doc = convert_from_path(file_path, fmt='jpg')[0]
        return doc
    except Exception as e:
        print("An error occurred:", e)

def extract_data(cropped_image):
    extracted_text = pytesseract.image_to_string(cropped_image, config='--oem 3 --psm 4')    
    compiled = re.compile(re.escape("\n"), re.IGNORECASE)
    cleaned_text = compiled.sub("", extracted_text)
    return cleaned_text

def extract_amount(cropped_image):
    extracted_text = pytesseract.image_to_string(cropped_image, config='--oem 3 --psm 4')
    amountRegex = r'\b\d{2}\,\d{2}\b'    
    return re.findall(amountRegex, extracted_text)[0]

app = Flask(__name__)

@app.route('/')
def main():
    try:
        file_path = 'C:/Users/PcCentar/Desktop/repos/bank_statements_ocr/bank_statements/rzzeport.pdf'
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

        main_json = {
            "order_number": extract_data(thresh[c.order_number['start_y']:c.order_number['end_y'], c.order_number['start_x']:c.order_number['end_x']]),
            "sender": extract_data(thresh[c.sender['start_y']:c.sender['end_y'], c.sender['start_x']:c.sender['end_x']]),
            "sender_address": extract_data(thresh[c.sender_address['start_y']:c.sender_address['end_y'], c.sender_address['start_x']:c.sender_address['end_x']]),
            "sender_city": extract_data(thresh[c.sender_city['start_y']:c.sender_city['end_y'], c.sender_city['start_x']:c.sender_city['end_x']]),
            "receiver": extract_data(thresh[c.receiver['start_y']:c.receiver['end_y'], c.receiver['start_x']:c.receiver['end_x']]),
            "receiver_address": extract_data(thresh[c.receiver_address['start_y']:c.receiver_address['end_y'], c.receiver_address['start_x']:c.receiver_address['end_x']]),
            "receiver_city": extract_data(thresh[c.receiver_city['start_y']:c.receiver_city['end_y'], c.receiver_city['start_x']:c.receiver_city['end_x']]),
            "purpose_of_remittance": extract_data(thresh[c.purpose_of_remittance['start_y']:c.purpose_of_remittance['end_y'], c.purpose_of_remittance['start_x']:c.purpose_of_remittance['end_x']]),
            "sender_bank_account": extract_data(thresh[c.sender_bank_account['start_y']:c.sender_bank_account['end_y'], c.sender_bank_account['start_x']:c.sender_bank_account['end_x']]),
            "receiver_bank_account": extract_data(thresh[c.receiver_bank_account['start_y']:c.receiver_bank_account['end_y'], c.receiver_bank_account['start_x']:c.receiver_bank_account['end_x']]),
            "payment_date": extract_data(thresh[c.payment_date['start_y']:c.payment_date['end_y'], c.payment_date['start_x']:c.payment_date['end_x']]),
            "amount": extract_amount(thresh[c.amount['start_y']:c.amount['end_y'], c.amount['start_x']:c.amount['end_x']])
        }

        return json.dumps(main_json)
    except Exception as e:
        return "An error occurred:" + str(e)
