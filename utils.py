
import json


def print_json(json_obj, sort=True, indents=4):

    if type(json_obj) is str:
        print(json.dumps(json.loads(json_obj), sort_keys=sort, indent=indents))

    else:
        print(json.dumps(json_obj, sort_keys=sort, indent=indents))

    return None
