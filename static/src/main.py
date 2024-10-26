"""
Application:

    QRORK 
    Version 0.1.0


Description:

    Generate a QR code using python

    
Install dependencies:

    pip install "qrcode[pil]"
"""


###----------------------->>>>>>>
# import libraries
import os
import qrcode
import re


###----------------------->>>>>>>
# define constansts
DIR = 'codes'
IMG_FORMATS = ['PNG', 'JPEG', 'BMP', 'GIF', 'TIFF', 'WEBP']


###----------------------->>>>>>>
# user input prompt: url
def get_url():

    while True:
        url = input('\nWhere would you like the QR code to lead to?\nPlease enter a valid URL starting with http:// or https://\n >> ')
        
        if validate_url(url):
            return url


###----------------------->>>>>>>
# validates user input against regex for valid URL formats (starting with http:// or https://).
def validate_url(url):

    pattern = re.compile(
        # http:// or https://
        r'^(https?:\/\/)'
        # domain name                         
        r'([\da-z.-]+)\.([a-z.]{2,6})'
        # path            
        r'([\/\w .-]*)*'
        # query parameters                         
        r'(\?[\/\w=&.-]*)?$',
    )

    if len(url) > 512:
        print("Invalid URL. Please enter a URL that is less than 512 characters.")
        return False
    
    if re.match(pattern, url):
        return True
    
    print("Invalid URL. Please enter a valid URL starting with http:// or https://")
    return False


###----------------------->>>>>>>
# user input prompt: file
def get_file():

    while True:
        file = input('\nWhat would you like to name this file?\nPlease use only letters, numbers, spaces, underscores, hyphens, and periods.\n >> ')
        
        if validate_file(file):
            return file


###----------------------->>>>>>>
# validates user input against regex for valid filename characters (letters, numbers, spaces, underscores, hyphens, and periods).
def validate_file(file):
    
    if re.match(r'^[\w\-. ]+$', file) and len(file) > 0:
        return True
    
    print("Invalid file name. Only letters, numbers, spaces, underscores, hyphens, and periods are allowed.")
    return False


###----------------------->>>>>>>
# user input prompt: format
def get_format():

    while True:
        format = input(f"\nWhat file format would you like to save?\nPlease choose from {', '.join(IMG_FORMATS)}.\n >> ")
        
        if validate_format(format.upper()):
            return format.upper()


###----------------------->>>>>>>
# validates user input against predefined QR code format options (PNG, JPEG, BMP, GIF, TIFF, WEBP).
def validate_format(format):
    
    if format not in IMG_FORMATS:
        print(f"Invalid format. Please choose from {', '.join(IMG_FORMATS)}.")
        return False
    
    return True


###----------------------->>>>>>>
#
def display_title():
    print(
"""
|-----------------------------------|
|               QRORK               |
|                                   |
|         QR Code Generator         |
|           Version 0.1.0           |
| ©2024 Almond House Publishing LLC |
|    Developed by David Blessent    |
|-----------------------------------|
"""
    )
    input(' >> Press [ENTER] to begin ')


###----------------------->>>>>>>
# script for generating a QR code via user inputs
def main():

    if not os.path.exists(DIR):
        os.makedirs(DIR)

    display_title()

    url = get_url()
    file = get_file()
    format = get_format()

    file_name = f"{file}.{format.lower()}"
    path = os.path.join(DIR, file_name)

    try:
        img = qrcode.make(url)
        img.save(path, format=format)
    except Exception as e:
        print(f"An error occured while saving the QR code: {e}")

    print(f"\nSuccess!\n\nQR code saved to: {path}")


if __name__ == "__main__":

    main()