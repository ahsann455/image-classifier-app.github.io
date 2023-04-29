# Import necessary modules
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import os
from app_helper import *

# Create Flask app instance
app = Flask(__name__)

# Define route to display the index page
@app.route("/")
def index():
    return render_template("index.html")

# Define route to handle file upload
@app.route('/uploader', methods = ['POST'])
def upload_file():
    predictions=""

    if request.method == 'POST':
        f = request.files['file']

        # Save the file to the uploads folder
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(basepath, 'static','uploads', secure_filename(f.filename))
        f.save(file_path)

        # Get class predictions
        predictions = get_classes(file_path)
        pred_strings = []
        for _,pred_class,pred_prob in predictions:
            pred_strings.append(str(pred_class).strip()+" : "+str(round(pred_prob*100,2)).strip()+"%")
        preds = ", ".join(pred_strings)

    # Render the upload.html template with predictions and uploaded image
    return render_template("upload.html", predictions=preds, display_image=f.filename) 

# Start the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True,port="4100")
