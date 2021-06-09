import json


def get_json_data(file_path: str) -> list:
    """
    Returns list of dictionaries from json file.
    :param file_path: string
    :return: list
    """
    with open(file_path, 'r') as file:
        return json.load(file)
