from os import path

from flask import Flask
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from flask_restx import Resource, Api, fields

from .excel_summary import process_excel_file
from .messages import NO_FILE_MSG, INCORRECT_FILE_NAME_MSG, INCORRECT_FILE_EXTENSION_MSG, NO_EXCEL_COLUMN_MSG,\
    ERROR_DURING_FILE_PROCESSING_MSG, DUPLICATED_PARAMETERS_MSG
from .utils import has_duplicates

app = Flask(__name__)
app.config['UPLOAD_EXTENSIONS'] = ['.xlsx']
app.config['JSON_SORT_KEYS'] = False
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
api = Api(app, doc='/apidocs', version='1.0.0', title='Excel Summary API')

upload_parser = api.parser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True)
upload_parser.add_argument('columns', location='form', type=str, action='append', required=True)


@api.route('/summary')
class Summary(Resource):
    @api.doc(parser=upload_parser)
    def post(self):
        args = upload_parser.parse_args()
        if 'file' not in args:
            return dict(error=NO_FILE_MSG), 400

        uploaded_file = args.get('file')
        if not uploaded_file:
            return dict(error=NO_FILE_MSG), 400

        if not uploaded_file.filename:
            return dict(error=NO_FILE_MSG), 400

        file_name = secure_filename(uploaded_file.filename)
        if not file_name:
            return dict(error=INCORRECT_FILE_NAME_MSG), 400

        file_extension = path.splitext(file_name)[1]
        if file_extension not in app.config['UPLOAD_EXTENSIONS']:
            return dict(error=INCORRECT_FILE_EXTENSION_MSG), 400

        if 'columns' not in args:
            return dict(error=NO_EXCEL_COLUMN_MSG), 400

        columns = args.get('columns')
        if not columns:
            return dict(error=NO_EXCEL_COLUMN_MSG), 400

        if has_duplicates(columns):
            return dict(error=DUPLICATED_PARAMETERS_MSG), 400

        try:
            return process_excel_file(uploaded_file, file_name, columns)
        except Exception as ex:
            app.logger.error(str(ex))
            return dict(error=ERROR_DURING_FILE_PROCESSING_MSG), 500
