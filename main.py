import os
from flask import Flask, jsonify, request, send_from_directory, current_app, render_template
from werkzeug.utils import secure_filename
from datetime import datetime, timezone
import zipfile

app = Flask(__name__)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        LOGFILEPATH=os.path.join(app.instance_path, 'logs'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # Check for the instance folder and create
    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)

    # Check for the instance folder and create
    if not os.path.exists(app.config['LOGFILEPATH']):
        os.makedirs(app.config['LOGFILEPATH'])

    @app.route('/uploadlog', methods=['POST'])
    def upload():
        if request.method == 'POST':
            file = request.files['']
            file_name, file_ext = file.filename.split('.')
            file_string = f'{file_name}_{datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M")}.{file_ext}'
            file.save(os.path.join(app.config['LOGFILEPATH'], secure_filename(file_string)))
            return 'file uploaded successfully'

    @app.route('/logs', methods=['GET'])
    def list_logs():
        files = os.listdir(app.config['LOGFILEPATH'])
        return render_template('directory_template.html', files=files)

    @app.route('/logs/<path:filename>', methods=['GET'])
    def download(filename):
        if filename in os.listdir(app.config['LOGFILEPATH']):
            return send_from_directory(app.config['LOGFILEPATH'], filename, as_attachment=True)
        else:
            return 'file not found'

    @app.route('/pull_logs', methods=['GET'])
    def pull_logs():
        with zipfile.ZipFile('logs.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(app.config['LOGFILEPATH']):
                for file in files:
                    zipf.write(os.path.join(app.config['LOGFILEPATH'], file), file)
        return send_from_directory(current_app.root_path, 'logs.zip', as_attachment=True)

    return app


if __name__ == "__main__":
    create_app().run(host='0.0.0.0', debug=True)

