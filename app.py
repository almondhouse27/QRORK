from flask      import Flask, render_template, request, send_file, flash
from qr_utils   import validate_url, validate_file, validate_format, generate
from dotenv     import load_dotenv
import os
import logging
import threading

# STARTUP & CONFIGURATION 
###----------------------->>>>>>>
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

# ROUTING
###----------------------->>>>>>>
"""
ROUTE:      '/'
TEMPLATE:   index.html
NAVLINK:    Tool
PURPOSE:    index() renders the Tool page @click=navlink (GET)
            downloads a QR code @click=submit            (POST)
            preview QR code modal @click=preview         (POST)
""" 
@app.route("/", methods=["GET", "POST"])
def index():

    # initialize variables
    url = ""
    file_name = ""
    export_format = ""
    color = "default"
    qr_image_url = None

    # fetch user input from form on 'submit'
    if request.method == "POST":
        logging.debug("Form data: %s", request.form) 
        url = request.form["url"]
        file_name = request.form["file-name"]
        export_format = request.form["export-format"]
        color = request.form.get("color", "default")

        # validate user input, generate image, and instantiate QR code file
        if validate_url(url) and validate_file(file_name) and validate_format(export_format):
            file_path = generate(url, file_name, export_format, color)

            # when submit button is clicked with valid user input
            if 'submit' in request.form:
                response = send_file(file_path, as_attachment=True)
                os.remove(file_path)
                return response
            
            # when preview button is clicked with valid user input
            elif 'preview' in request.form:

                if os.path.exists(file_path):
                    threading.Timer(5.0, os.remove, [file_path]).start()
                    # threading.Thread(target=lambda: (time.sleep(5), os.remove(file_path))).start()
                    return render_template(
                        "index.html", 
                        url = request.form["url"], 
                        file_name = request.form["file-name"], 
                        export_format = request.form["export-format"],
                        color = request.form["color"],
                        qr_image_url = f'codes/{file_name}.{export_format.lower()}'
                    )

        # validation fails, flash how-to message
        else:
            flash("Please provide valid input for all fields.\nEnter a valid URL starting with http:// or https://, up to 512 characters.\nUse only letters, numbers, spaces, underscores, hyphens, and periods for the file name.")

    # if request.method="GET"
    return render_template("index.html")

###----------------------->>>>>>>
"""
ROUTE:      '/about'
TEMPLATE:   about.html
NAVLINK:    About
PURPOSE:    about() renders the About page @click=navlink (GET)
""" 

###----------------------->>>>>>>
"""
ROUTE:      '/store'
OFFSITE:    https://almondhousepublishing.com
NAVLINK:    Store
PURPOSE:    redirects to official Almond House Publishing store
""" 

###----------------------->>>>>>>
"""
ROUTE:      '/code'
OFFSITE:    https://github.com/almondhouse27
NAVLINK:    About
PURPOSE:    redirects to QRORK github repository
""" 

if __name__ == "__main__":
    app.run(debug=True)
