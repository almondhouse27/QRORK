from flask              import Flask, render_template, request, send_file, flash, redirect, url_for
from flask_caching      import Cache
from flask_limiter      import Limiter
from flask_limiter.util import get_remote_address
from dotenv             import load_dotenv
from qr_utils           import validate_url, validate_file, validate_format, generate, delete_codes
import os
import logging
import threading


# STARTUP & CONFIGURATION 
###----------------------->>>>>>>
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

limiter = Limiter(get_remote_address, app=app)

cache = Cache(app)
cache_cleared = False
@app.before_request
def clear_cache():
    global cache_cleared
    if not cache_cleared:
        cache.clear()
        cache_cleared = True

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log", mode='w'),
        logging.StreamHandler()
    ]
)

threading.Thread(target=delete_codes, daemon=True).start()

# ERROR HANDLER
###----------------------->>>>>>>
@app.errorhandler(429)
def ratelimit(error):

    return render_template('ratelimit.html'), 429

@app.route("/reset")
def reset():

    limiter.reset()
    return redirect(url_for("index"))


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
@limiter.limit("10 per minute")
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
        url_valid = validate_url(url)
        file_valid = validate_file(file_name)
        format_valid = validate_format(export_format)

        if url_valid and file_valid and format_valid:
            file_path = generate(url, file_name, export_format, color)

            # when submit button is clicked with valid user input
            if 'submit' in request.form:
                response = send_file(file_path, as_attachment=True)
                return response
            
            # when preview button is clicked with valid user input
            elif 'preview' in request.form:

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
            if not url_valid:
                flash("INVALID URL")
            
            if not file_valid:
                flash("INVALID FILE NAME")

            return render_template(
                "index.html", 
                url=url, 
                file_name=file_name, 
                export_format=export_format, 
                color=color
            )
        
    # if request.method="GET"
    return render_template("index.html")


###----------------------->>>>>>>
"""
ROUTE:      '/about'
TEMPLATE:   about.html
NAVLINK:    About
PURPOSE:    about() renders the About page @click=navlink (GET)
"""
@app.route('/about')
def about():
    ##flash('About page coming soon!')
    ##return redirect(url_for('index'))
    return render_template("about.html")


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
NAVLINK:    Code
PURPOSE:    redirects to QRORK github repository
""" 


if __name__ == "__main__":
    app.run(debug=True)
