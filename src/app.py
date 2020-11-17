import subprocess
import sys
import os
try: 
    from flask import Flask, render_template, request, redirect, url_for, abort, \
    send_from_directory
    import imghdr
    from werkzeug.utils import secure_filename
except ImportError: 
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'flask'])   
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'flask_cors']) 
finally: 
    from flask import Flask, render_template, request, redirect, url_for, abort, \
    send_from_directory

    """
    subprocess -store the return code to execute in systerm and display the output. 
    flask_cors - A Flask extension for handling Cross Origin Resource Sharing (CORS), making cross-origin AJAX possible. 
    This package has a simple philosophy: when you want to enable CORS, you wish to enable 
    it for all use cases on a domain. This means no mucking around with different allowed headers, methods, etc.

    """

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 # set constraints for image size
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif'] # set only image file types to accept
app.config['UPLOAD_PATH'] = 'uploads' # where to upload images
# C- create R- read U- update D -delete
def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

#This Route is to send an error for images to large to process.
@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_PATH'])
    return render_template('index.html', files=files)

@app.route('/', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                file_ext != validate_image(uploaded_file.stream):
            return "Invalid image", 400
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    return '', 204

@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)

# @app.route('/deploy/')
# def upload(filename):
#     return 


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)