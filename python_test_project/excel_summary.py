from enum import Enum
from pandas import ExcelFile, to_numeric
from .messages import WRONG_EXCEL_FORMAT_MSG, COLUMN_NOT_FOUND_MSG
from .utils import replace_nan


class ProcessStatus(Enum):
    SUCCESS = 'success'
    ERROR = 'error'


def is_column_in_summary(summary_list, column_name):
    for summary in summary_list:
        if summary['column'] == column_name:
            return True
    return False


def process_excel_file(file, file_name, column_list):
    try:
        excel = ExcelFile(file)
    except:
        return dict(error=WRONG_EXCEL_FORMAT_MSG), 400

    response_dict = {
        'file': file_name,
        'summary': []
    }

    summary_response_template = {
        'column': '',
        'status': ProcessStatus.ERROR.value,
        'message': COLUMN_NOT_FOUND_MSG,
        'sheet': None,
        'columnOrder': None,
        'sum': None,
        'avg': None
    }

    for sheet_index, sheet in enumerate(excel.sheet_names):
        data_frame = excel.parse(sheet_index)
        if data_frame.empty:
            continue

        for column_name in column_list:
            if not column_name:
                continue

            filtered_column_list = [column for column in data_frame if data_frame[column].astype(str).str.contains(
                column_name).any()]

            for column_index, column in enumerate(filtered_column_list):
                numeric_data_frame = to_numeric(data_frame[filtered_column_list[column_index]], errors='coerce')
                column_order = list(data_frame.columns).index(column) + 1

                column_sum = replace_nan(numeric_data_frame.sum(skipna=True), 0)
                column_avg = replace_nan(numeric_data_frame.mean(skipna=True), 0)

                summary_response = summary_response_template.copy()
                summary_response['column'] = column_name
                summary_response['status'] = ProcessStatus.SUCCESS.value
                summary_response['message'] = ''
                summary_response['sheet'] = sheet
                summary_response['columnOrder'] = column_order
                summary_response['sum'] = column_sum
                summary_response['avg'] = column_avg

                response_dict['summary'].append(summary_response)

    for column_name in column_list:
        if not is_column_in_summary(response_dict['summary'], column_name):
            default_response_summary = summary_response_template.copy()
            default_response_summary['column'] = column_name
            response_dict['summary'].append(default_response_summary)

    return dict(response_dict), 200
