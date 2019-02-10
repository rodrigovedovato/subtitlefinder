import json

def toJson(dictionary):
    return json.loads(json.dumps(dictionary, ensure_ascii=False))