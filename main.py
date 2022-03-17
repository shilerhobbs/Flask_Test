from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = '/home/logs/'
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
        print(request.files[0])
        f = request.files['file']
        f.save(secure_filename(f.filename))
        return 'file uploaded successfully'

if __name__ == "__main__":
    app.run(host = '0.0.0.0', debug=True)