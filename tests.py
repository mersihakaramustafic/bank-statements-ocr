import unittest
from app import extract_data, extract_amount # upload_pdf, detect_report_type,
 
# Define class to test the program
class TestTextExtraction(unittest.TestCase):
    # Function to test addition function
    def test_upload_pdf(self):
        result = addition(2, 2)
        self.assertEqual(result, 4)

        #./files/test.pdf
         
    # Function to test addition function
    def test_detect_report_type(self):
        result = subtraction(4, 2)
        self.assertEqual(result, 2)
         
   # Function to test addition function
    def test_extract_data(self):
        result = multiplication(2, 3)
        self.assertEqual(result, 6)
         
    # Function to test addition function
    def test_extract_amount(self):
        result = division(4, 2)
        self.assertEqual(result, 2)
 
if __name__ == '__main__':
    unittest.main()