import json


def json_demo():
    data = {"name": "Лаба 4", "files": 16}
    text = json.dumps(data, ensure_ascii=False)
    return json.loads(text)