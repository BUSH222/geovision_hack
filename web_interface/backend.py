import os
import time

from flask import Flask, flash, request, redirect, url_for,render_template
from werkzeug.utils import secure_filename
from PIL import Image
import fitz
import shutil
from gisprocessor import GeneralConverter

UPLOAD_FOLDER = r'D:\Новая папка'
ALLOWED_EXTENSIONS = {'txt', 'png', 'jpg', 'jpeg','gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


config = []



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):

            filename = secure_filename(file.filename)

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            if '.txt' in filename:
                config.append(os.path.join(UPLOAD_FOLDER,filename))
            else:
                res = GeneralConverter(os.path.join(UPLOAD_FOLDER,filename),'D:\Новая папка (2)')
                res.load_from_json(config[0])
                res.run()



    return render_template('main_page.html')


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=86, debug=False)


