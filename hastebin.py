import requests
import json


class HasteBinApi:

    def __init__(self, content):
        self.content = content

    def get_key(self):
        req = requests.post('https://hastebin.com/documents',
                            # headers={},
                            data=self.content)

        key = json.loads(req.content)
        return key['key']
