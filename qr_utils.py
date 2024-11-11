import logging
import os
import qrcode
import re
import time
import threading

DIR = os.path.join('static', 'codes')
IMG_FORMATS = ['PNG', 'JPEG', 'BMP', 'GIF', 'TIFF', 'WEBP']


# validates user input against regex for valid URL formats (starting with http:// or https://)
def validate_url(url):

    pattern = re.compile(
        r'^(https?:\/\/)'                 # http:// or https://                 
        r'([\da-z.-]+)\.([a-z.]{2,6})'    # domain name 
        r'([\/\w .@-]*)*'                 # path               
        r'(\?[\/\w=&.-]*)?$',             # query parameters   
    )
    return re.match(pattern, url) and len(url) <= 512


# validates user input against regex for valid filename characters (letters, numbers, spaces, underscores, hyphens, and periods)
def validate_file(file):

    return re.match(r'^[\w\-. ]+$', file) and len(file) > 0


# validates user input against predefined QR code format options (IMG_FORMATS)
def validate_format(format):

    return format.upper() in IMG_FORMATS


# handles timeout exception to prevent hangup
def timeout_handler(signum, frame):

    raise Exception("QR code generation took too long")


# generates a qr code based on user inputs
def generate(url, file_name, export_format, color='default'):

    timeout = 10
    timer = threading.Timer(timeout, timeout_handler)
    timer.start()

    if not os.path.exists(DIR):

        os.makedirs(DIR)

    file_path = f"{DIR}/{file_name}.{export_format.lower()}"

    try:

        if color == "default":
            img = qrcode.make(url)
            
        else:    
            if color == "invert":
                fore = "white"
                back = "black"
            elif color == "bee":
                fore = "black"
                back = "yellow"
            elif color == "jungle":
                fore = "darkgreen"
                back = "lightgreen"

            qr = qrcode.QRCode()
            qr.add_data(url)
            qr.make(fit=True)
            img = qr.make_image(fill_color=fore, back_color=back)

        img.save(file_path, format=export_format.lower())
        logging.info("Generated QR code saved at: %s", file_path)
        return file_path
    
    except Exception as e:
        logging.error(f"Error generating QR code: {e}")
        raise 
    
    finally:
        timer.cancel()


# generates a qr code based on user inputs
def delete_codes():
        
        while True:
            current_time = time.time()

            for filename in os.listdir(DIR):
                file_path = os.path.join(DIR, filename)

                if os.path.isfile(file_path) and current_time - os.path.getmtime(file_path) > 180:
                    os.remove(file_path)
                    logging.info("Deleted old QR code: %s", file_path)

            time.sleep(180)
