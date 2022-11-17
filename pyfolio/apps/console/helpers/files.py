import json


def read_json_file(file_path: str):
    with open(file_path) as json_file:
        data = json.load(json_file)
        return data

