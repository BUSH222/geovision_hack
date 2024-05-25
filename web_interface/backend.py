import os
from flask import Flask, flash, request, redirect, url_for,render_template
from werkzeug.utils import secure_filename
from PIL import Image
import fitz
import shutil

UPLOAD_FOLDER = r'D:\Новая папка'
ALLOWED_EXTENSIONS = {'txt', 'png', 'jpg', 'jpeg','gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



def pil_convert(path, dpi=300):
    ext = os.path.splitext(path)[-1].lower()
    if ext == '.png' or ext == '.jpg':
        return Image.open(path)
    elif ext == '.pdf':
        doc = fitz.open(path)
        page = doc.load_page(0)
        pixmap = page.get_pixmap(dpi=dpi)
        width, height = pixmap.width, pixmap.height
        img_bytes = pixmap.samples
        shutil.move(Image.frombytes("RGB", (width, height), img_bytes),'')
    else:
        return None

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
                pass
            else:
                res = pil_convert(os.path.join(UPLOAD_FOLDER,filename))
                print(res)
    return render_template('main_page.html')


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=86, debug=False)


