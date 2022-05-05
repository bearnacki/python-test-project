from numpy import nan


def has_duplicates(input_list):
    return len(input_list) != len(set(input_list))


def replace_nan(value, replace_value):
    if value is nan:
        return replace_value
    return value
