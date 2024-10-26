import logging
import os
import qrcode
import re

DIR = 'static/codes'
IMG_FORMATS = ['PNG', 'JPEG', 'BMP', 'GIF', 'TIFF', 'WEBP']

###----------------------->>>>>>>
# validates user input against regex for valid URL formats (starting with http:// or https://).
def validate_url(url):
    pattern = re.compile(
        r'^(https?:\/\/)'                   # http:// or https://                 
        r'([\da-z.-]+)\.([a-z.]{2,6})'      # domain name 
        r'([\/\w .@-]*)*'                   # path               
        r'(\?[\/\w=&.-]*)?$',               # query parameters   
    )
    return re.match(pattern, url) and len(url) <= 512

###----------------------->>>>>>>
# validates user input against regex for valid filename characters (letters, numbers, spaces, underscores, hyphens, and periods).
def validate_file(file):
    return re.match(r'^[\w\-. ]+$', file) and len(file) > 0

###----------------------->>>>>>>
# validates user input against predefined QR code format options (IMG_FORMATS).
def validate_format(format):
    return format.upper() in IMG_FORMATS

###----------------------->>>>>>>
# generates a qr code based on user inputs
def generate(url, file_name, file_format):
    if not os.path.exists(DIR):
        os.makedirs(DIR)
    img = qrcode.make(url)
    file_path = f"{DIR}/{file_name}.{file_format.lower()}"
    img.save(file_path, format=file_format.lower())
    logging.info("Generated QR code saved at: %s", file_path)
    return file_path
