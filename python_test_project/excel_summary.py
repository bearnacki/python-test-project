from flask import jsonify
from pandas import ExcelFile, to_numeric


def process_excel_file(file, file_name, column_list):
    response_dict = {
        'file': file_name,
        'summary': []
    }

    excel = ExcelFile(file)
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
                column_sum = numeric_data_frame.sum(skipna=True)
                column_avg = numeric_data_frame.mean(skipna=True)
                response_dict['summary'].append({
                    'column': column_name,
                    'sheet': sheet,
                    'columnOrder': column_order,
                    'sum': column_sum,
                    'avg': column_avg,
                })

    return jsonify(response_dict), 200
