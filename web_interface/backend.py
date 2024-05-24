from flask import Flask, request, send_file,render_template
import os

from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join('uploads', filename))
        return f'File {filename} uploaded successfully.'
    return render_template('main_page.html')


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=86, debug=False)


