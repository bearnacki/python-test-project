from flask import jsonify
from pandas import ExcelFile, to_numeric


def process_excel_file(file, file_name, column_list):
    response_dict = {
        'file': file_name,
        'summary': []
    }

    excel = ExcelFile(file)
    for index, sheet in enumerate(excel.sheet_names):
        data_frame = excel.parse(index)
        if data_frame.empty:
            continue

        for column_name in column_list:
            filtered_column_list = [column for column in data_frame if data_frame[column].astype(str).str.contains(
                column_name).any()]
            if filtered_column_list:
                numeric_data_frame = to_numeric(data_frame[filtered_column_list[0]], errors='coerce')
                column_sum = numeric_data_frame.sum(skipna=True)
                column_avg = numeric_data_frame.mean(skipna=True)
                response_dict['summary'].append({
                    'column': column_name,
                    'sum': column_sum,
                    'avg': column_avg
                })

    return jsonify(response_dict), 200
