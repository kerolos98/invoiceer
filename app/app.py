from flask import Flask, render_template, request, redirect, url_for,send_file
import os
import logging
from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath
from invoice_extractor import perform_ocr , get_data_regex
import json

app = Flask(__name__, static_folder='static', static_url_path='/static')
UPLOADS_PATH = join(dirname(realpath(__file__)), 'static/uploads/..')
app.config['UPLOAD_FOLDER'] = UPLOADS_PATH

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' in request.files:
        image = request.files['image']
        if image.filename != '':
            filename = secure_filename(image.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print("Saving file to:", save_path)
            image.save(save_path)
            # Pass invoice_data as a dictionary to the show_image route
            return redirect(url_for('show_image', filename=filename))
    return 'No image uploaded.'


@app.route('/uploads/<filename>')
def show_image(filename):
    # Perform OCR and extract data from the image
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    ocr = perform_ocr(save_path)
    invoice_data = get_data_regex(ocr)
    # Pass invoice_data as a dictionary to the show_image template
    return render_template('show_image.html', filename=filename, data=invoice_data)

if __name__ == '__main__':
    app.run(debug=False, port=5000, host='0.0.0.0')  # nosec

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)