import json
from os import path

from flask import Flask, jsonify, request
from flasgger import Swagger
from werkzeug.utils import secure_filename

from .excel_summary import process_excel_file
from .messages import NO_FILE_MSG, INCORRECT_FILE_NAME_MSG, INCORRECT_FILE_EXTENSION_MSG, NO_EXCEL_COLUMN_MSG,\
    ERROR_DURING_FILE_PROCESSING_MSG

app = Flask(__name__)
app.config['UPLOAD_EXTENSIONS'] = ['.xlsx']
app.config['JSON_SORT_KEYS'] = False
swagger = Swagger(app)


@app.route('/')
def index():
    return jsonify({'message': 'Welcome to Excel Summary API'}), 200


@app.route('/summary', methods=['POST'])
def summary():
    """Returns excel file summary
    ---
    parameters:
      - in: formData
        name: file
        type: file
        required: true
        description: The file to upload.
      - in: formData
        name: column
        type: array
        items:
          - type: string
        required: true
        description: Excel file column name to perform a summary.
    definitions:
      SummaryItem:
        properties:
          column:
            type: string
          sheet:
            type: string
          columnOrder:
            type: integer
          sum:
            type: number
          avg:
            type: number
      Summary:
        type: object
        properties:
          file:
            type: string
          summary:
            type: array
            items:
              $ref: '#/definitions/SummaryItem'
      Error:
        type: object
        properties:
          error:
            type: string
    responses:
      200:
        description: Summary of columns values in excel file
        schema:
          $ref: '#/definitions/Summary'
      400:
        description: Bad request
        schema:
          $ref: '#/definitions/Error'
      500:
        description: Internal server error
        schema:
          $ref: '#/definitions/Error'
    """
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

    columns = request.form.get('column')
    if not columns:
        return jsonify(error=NO_EXCEL_COLUMN_MSG), 400

    try:
        column_list = json.loads('[' + columns + ']')
        return process_excel_file(uploaded_file, file_name, column_list)
    except Exception as ex:
        app.logger.error(str(ex))
        return jsonify(error=ERROR_DURING_FILE_PROCESSING_MSG), 500
