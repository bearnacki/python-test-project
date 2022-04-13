from os import path

from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename

from .excel_summary import process_excel_file
from .messages import NO_FILE_MSG, INCORRECT_FILE_NAME_MSG, INCORRECT_FILE_EXTENSION_MSG, NO_EXCEL_COLUMN_MSG,\
    ERROR_DURING_FILE_PROCESSING_MSG

app = Flask(__name__)
app.config['UPLOAD_EXTENSIONS'] = ['.xlsx']
app.config['UPLOAD_PATH'] = 'uploads'
app.config['JSON_SORT_KEYS'] = False


@app.route('/')
def index():
    return jsonify({'message': 'Welcome to Excel Summary API'}), 200


@app.route('/summary', methods=['POST'])
def summary():
    if 'file' not in request.files:
        return jsonify(error=NO_FILE_MSG), 400

    uploaded_file = request.files['file']
    if not uploaded_file.filename:
        return jsonify(error=NO_FILE_MSG), 400

    file_name = secure_filename(uploaded_file.filename)
    if not file_name:
        return jsonify(error=INCORRECT_FILE_NAME_MSG), 400

    file_extension = path.splitext(file_name)[1]
    if file_extension not in app.config['UPLOAD_EXTENSIONS']:
        return jsonify(error=INCORRECT_FILE_EXTENSION_MSG), 400

    column_list = request.form.getlist('column')
    if not column_list:
        return jsonify(error=NO_EXCEL_COLUMN_MSG), 400

    try:
        return process_excel_file(uploaded_file, file_name, column_list)
    except Exception as ex:
        app.logger.error(str(ex))
        return jsonify(error=ERROR_DURING_FILE_PROCESSING_MSG), 500
