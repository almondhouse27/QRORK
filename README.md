# QRORK - QR Code Generator


## Description

**QRORK** is a simple QR code generator built using Python

The program allows users to create QR codes that link to specified URLs, saving them in various image formats


## Features

- Generate QR codes for any valid URL
- Save QR codes in multiple formats: PNG, JPEG, BMP, GIF, TIFF, WEBP
- User-friendly prompts for input


## Prerequisites

Ensure you have Python installed on your system. This project requires Python 3.x

Dependencies for **QRORK** are recorded in `requirements.txt`


## Installation

### Clone the Repository

To clone the project - open your terminal, navigate to the destination directory, and run:

```bash
   git clone https://github.com/almondhouse27/QRORK.git
```

### Set up Virtual Environment

To set up a virtual environment - open your terminal, navigate to the project root, and run:

```bash
   python3 -m venv venv
```

To activate the virtual environment run:

On Mac
```bash
   source venv/bin/activate
```

On Windows
```bash
   .\venv\Scripts\activate 
```

*Using a virtual environment ensures that the project dependencies are installed locally, specific to this project*

### Dependencies

To install the project dependencies - open your terminal, navigate to the project root, and run:

```bash
   pip install -r requirements.txt
```


## Usage

### Command Line Application - QRORK

To run the command line version of **QRORK** -  navigate to the project root and run:

```bash
   python ./static/src/main.py 
```

`main.py` is a simple command line application that uses the Python qrcode package to generate qr codes based on user input
- User inputs are validated with regex
- The generated QR code image file is saved in `./static/codes`

### Web Application - QRORK.app

To run the web application version of **QRORK** - navigate to the project root and run:

```bash
   flask --app app run --port 5001
```

*I use port 5001 because of my development environment. You can select your own port or leave the option off.*

`QRORK.app` is a web application that uses the Python qr package to genereate qr code based on user input
- User inputs are validated with regex
- The generated QR code image file is saved in `./static/codes`
- There is a 10 request per minute rate limit set
- There is a 10 second request timeout set 
- The application automatically deletes codes that were generated more than 3 minutes ago every 3 minutes


## Documentation Links
[Flask Documentation](https://flask.palletsprojects.com/en/stable/)
[Werkzeug Documentation](https://werkzeug.palletsprojects.com/en/stable/)
[Jinja Documentation](https://jinja.palletsprojects.com/en/stable/)
[Click Documentation](https://click.palletsprojects.com/en/stable/)
[QR Code PDocumentation](https://pypi.org/project/qrcode/)


## Copyright

**QRORK**
QR Code Generator
*Version 0.1.0*
©2024 Almond House Publishing LLC
All Rights Reserved
Developed by David Blessent


## License

This project is licensed under the terms of the GNU General Public License v3.0 (GPL-3.0)
- Effective since 11/10/2024
- See the [COPYING.md](./COPYING.md) file for more details