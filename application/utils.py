import json


def load_json_from_file(file):
    try:
        with open(f"application/data/{file}", mode="r", encoding="utf8") as f:
            data = json.load(f)
    except FileNotFoundError:
        pass
    return data