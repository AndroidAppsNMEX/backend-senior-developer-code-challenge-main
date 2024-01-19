import json

def load_mock_data(path):
    f = path.open('r')
    return json.load(f)
