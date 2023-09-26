import json


DEFAULT_PATH = "release-manager-ui/data/"


def load_json_from_file(filename):
    try:
        with open(DEFAULT_PATH + filename, 'r', encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File '{DEFAULT_PATH + filename}' not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from file '{DEFAULT_PATH + filename}': {e}")
        return None


def save_json_to_file(data, filename):
    try:
        with open(DEFAULT_PATH + filename, 'w', encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        print(f"JSON data saved to '{DEFAULT_PATH + filename}'")
    except Exception as e:
        print(f"Error saving JSON to file '{DEFAULT_PATH + filename}': {e}")
