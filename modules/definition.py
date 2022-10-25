import json


def definition(arg1):
    f = open("dictionary.json")
    data = json.load(f)
    f.close()
    try:
        return f"Definition of {arg1}: {data[arg1.upper()]}"
    except KeyError:
        return f"{arg1} not found in dictionary"
