

def check_data_type(data):
    if isinstance(data, str):
        return 'str'
    elif isinstance(data, bool):
        return 'bool'
    elif isinstance(data, int):
        return 'int'
    elif isinstance(data, float):
        return 'float'
    else:
        return None

