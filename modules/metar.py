import requests
import os
import json


def metar(arg1):
    chars = "[]'"
    metarKey = os.getenv("METAR_KEY")
    metarUrl = f"https://api.checkwx.com/metar/{str(arg1.upper())}?x-api-key={metarKey}"

    req = requests.get(metarUrl)

    try:
        req.raise_for_status()
        resp = json.loads(req.text)
    except requests.exceptions.HTTPError as e:
        print(e)

    result = str(resp["data"])

    for x in chars:
        result = result.replace(x, "")

    return result
