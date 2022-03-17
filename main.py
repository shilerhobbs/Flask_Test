from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

upload_folder = './logs/'

app.config['UPLOAD_FOLDER'] = upload_folder
app.config['MAX_CONTENT_PATH'] = 500000

incomes = [
    {'description': 'salary', 'amount': 5000}
]

@app.route("/")
def hello_world():
    return "Hello world!!"

@app.route('/incomes')
def get_incomes():
    return jsonify(incomes)


@app.route('/incomes', methods=['POST'])
def add_income():
    incomes.append(request.get_json())
    return '', 204

@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print(request.files)
        f = request.files['']
        f.save(secure_filename(f.filename))
        return 'file uploaded successfully'

if __name__ == "__main__":
    app.run(host = '0.0.0.0', debug=True)