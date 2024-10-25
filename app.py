from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QRORK</title>
    <style>
        /* Style for the navbar */
        nav {
            background-color: #333;
            overflow: hidden;
            padding: 10px;
            text-align: center;
        }
        nav a {
            color: white;
            padding: 14px 20px;
            text-decoration: none;
            display: inline-block;
        }
        nav a:hover {
            background-color: #575757;
        }

        /* Style for the form and image containers */
        .container {
            display: flex;
            justify-content: space-between;
        }
        .form-container {
            width: 30%;
            float: left;
            margin-right: 20px;
        }
        .form-container form {
            display: flex;
            flex-direction: column;
        }
        .form-container input {
            margin-bottom: 10px;
            padding: 10px;
            font-size: 16px;
        }
        .image-container {
            width: 60%;
            float: right;
        }

        /* Clear floats after the containers */
        .clearfix::after {
            content: "";
            clear: both;
            display: table;
        }
    </style>
</head>
<body>

    <!-- Simple Navbar -->
    <nav>
        <a href="#">Link1</a>
        <a href="#">Link2</a>
        <a href="#">Link3</a>
        <a href="#">Link4</a>
    </nav>

    <!-- Main Content: Form on the left, Image on the right -->
    <div class="container clearfix">
        <div class="form-container">
            <form>
                <label for="url">URL:</label>
                <input type="text" id="url" name="url" placeholder="Enter URL">

                <label for="file-name">File Name:</label>
                <input type="text" id="file-name" name="file-name" placeholder="Enter File Name">

                <label for="export-format">Export Format:</label>
                <input type="text" id="export-format" name="export-format" placeholder="Enter Export Format">

                <input type="submit" value="Submit">
            </form>
        </div>

        <!-- Image Floating Right -->
        <div class="image-container">
            <img src="/static/concept-art/caveman-barry.png" 
                 alt="Caveman Barry, a prehistoric character depicted in a rugged, natural setting, showcasing his primitive attire and tools, evoking a sense of adventure and survival."
                 width="700px"
                 style="margin-left: 20px;">
        </div>
    </div>

</body>
</html>
"""

if __name__ == "__main__":
    app.run(debug=True)
