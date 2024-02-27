import cv2 as cv
import numpy as np
from pdf2image import convert_from_path
import matplotlib.pyplot as plt

def convert_pdf(file_path):
    pil_image = convert_from_path(file_path, fmt='jpg')
    return pil_image[0]

file_path = 'C:/Users/PcCentar/Desktop/bank_statements_ocr/bank_statements/report.pdf'

image = convert_pdf(file_path)
plt.imshow(image)
plt.show()