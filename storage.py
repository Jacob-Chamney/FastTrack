import json
import os

# -----------DATA----------#


def write_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def read_json(path):
    if not os.path.exists(path):
        return
    with open(path, "r") as f:
        data = json.load(f)
        return data
