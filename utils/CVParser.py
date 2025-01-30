import os
from utils.utils import *

class CVParser():
    def __init__(self):
        self.type = ''

    def parse(self, file_name):
        file_ext = file_name.split('.')[-1]
        if file_ext == 'docx':
            cv_data = parse_cv_docx(file_name)
        elif file_ext == 'pdf':
            cv_data = parse_cv_pdf(file_name)
            # print(cv_data)

        elif file_ext in ['png', 'jpg', 'jpeg']:
            cv_data = parse_cv_img(file_name)

        return cv_data
