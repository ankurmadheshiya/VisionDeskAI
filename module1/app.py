import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'avi', 'webm'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def home():
    preview = None

    if request.method == 'POST':
        if 'image_file' in request.files and request.files['image_file'].filename:
            uploaded_file = request.files['image_file']
            if allowed_file(uploaded_file.filename):
                filename = secure_filename(uploaded_file.filename)
                uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                preview = {'type': 'image', 'filename': filename}
            else:
                preview = {'error': 'Only image files are supported.'}
        elif 'video_file' in request.files and request.files['video_file'].filename:
            uploaded_file = request.files['video_file']
            if allowed_file(uploaded_file.filename):
                filename = secure_filename(uploaded_file.filename)
                uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                preview = {'type': 'video', 'filename': filename}
            else:
                preview = {'error': 'Only video files are supported.'}

    return render_template('index.html', preview=preview)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)
