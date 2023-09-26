import json


def load_json_from_file(file):
    with open(f"release-manager-ui/data/{file}", mode="r", encoding="utf8") as f:
        return json.load(f)
