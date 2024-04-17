import unittest
import cv2
import numpy as np
from pdf2image import convert_from_path
import pytesseract
import re
import app as a
import constants as c

file = convert_from_path('C:/Users/PcCentar/Desktop/repos/bank_statements_ocr/bank_statements/report1_new.pdf', fmt='jpg')[0]
image = np.array(file)
image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

class TestTextMethods(unittest.TestCase):    

    def test_order_number(self):
        self.assertEqual(a.extract_data(thresh[c.order_number['start_y']:c.order_number['end_y'], c.order_number['start_x']:c.order_number['end_x']]), 'DPY000000073601308')

    def test_sender_city(self):
        self.assertEqual(a.extract_data(thresh[c.sender_city['start_y']:c.sender_city['end_y'], c.sender_city['start_x']:c.sender_city['end_x']]), 'SARAJEVO')
    
    def test_amount(self):
        self.assertEqual(a.extract_amount(thresh[c.amount['start_y']:c.amount['end_y'], c.amount['start_x']:c.amount['end_x']]), '50,00')

if __name__ == '__main__':
    unittest.main()