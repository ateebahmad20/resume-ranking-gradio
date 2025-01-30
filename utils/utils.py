from pypdf import PdfReader
import docx2txt
import cv2 
import pytesseract
import json

def parse_cv_pdf(file_name):
    reader = PdfReader(file_name)
    number_of_pages = len(reader.pages)
    text = ''
    for i in range(number_of_pages):
        page = reader.pages[i]
        text = text + '\n'+ page.extract_text()
    return text

def parse_cv_docx(file_name):
    text = docx2txt.process(file_name)
    return text

def parse_cv_img(file_name):
    # Adding custom options
    img = cv2.imread(file_name)
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(img, config=custom_config)
    return text

def read_json(file_name):
    # Opening JSON file
    with open(file_name) as f:
        data = json.load(f)
  
    return data
