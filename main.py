from flask import Flask, jsonify, request, send_from_directory, current_app, render_template
from werkzeug.utils import secure_filename
import os
import zipfile

app = Flask(__name__)

log_folder_name = 'logs'
with app.app_context():
    upload_folder = os.path.join(current_app.root_path, log_folder_name)

if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

app.config['UPLOAD_FOLDER'] = upload_folder
app.config['MAX_CONTENT_PATH'] = 500000

# TODO add authentication!!! LDAP?


# TODO add file extension checking - only log files should be uploaded
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        for file in request.files.getlist(''):
            file.save(os.path.join(upload_folder, secure_filename(file.filename)))
        return 'file uploaded successfully'
    if request.method == 'GET':
        return 'nothing here yet'


@app.route('/logs', methods=['GET'])
def list_logs():
    files = os.listdir(upload_folder)
    return render_template('directory_template.html', files=files)

@app.route('/logs/<path:filename>', methods=['GET'])
def download(filename):
    if filename in os.listdir('./logs'):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    else:
        return 'file not found'


@app.route('/pull_logs', methods=['GET'])
def pull_logs():
    with zipfile.ZipFile('logs.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(upload_folder):
            for file in files:
                zipf.write(os.path.join(upload_folder, file), file)
    return send_from_directory(current_app.root_path, 'logs.zip', as_attachment=True)



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
