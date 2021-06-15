import json


# function to add to JSON
def json_write_adding(filename, key, dict1):
    with open(filename, "r+", encoding='utf-8') as f:
        data = json.load(f)
        data[key].append(dict1)
        f.seek(0)
        json.dump(data, f, indent=2)
    return None


def json_write(filename, dict1):
    with open(filename, "w", encoding='utf-8') as f:
        json.dump(dict1, f, indent=2)
    return None


def json_load(filename):
    with open(filename, "r", encoding='utf-8') as f:
        data = json.load(f)
    return data

