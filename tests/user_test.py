'''
Moduł do testów

Wykonuje podane zapytania do API i generuje plik html z ich rezultatami
'''


import requests
import json
import os
from datetime import datetime

from jinja2 import Environment, FileSystemLoader


env = Environment(loader=FileSystemLoader('tests'))
template = env.get_template('test_template.html')

BASE = 'http://localhost:5000/'


class Request:
    def __init__(self, method, endpoint: str, json: dict = None):
        self.func = method
        self.method = self.func.__name__.upper()
        self.endpoint = endpoint
        self.params = json
        self.response = None
        self.text = self.call()

    def call(self):
        self.response = self.func(BASE+self.endpoint, json=self.params)
        try:
            return json.dumps(json.loads(self.response.text), indent=4)
        except:
            return self.response.text

    def get_params(self):
        return self.params
        requests.request()


reqs = (
    Request(requests.put, 'user', {'nick': 'alala',
                            'email': 'alala@test.com', 'password': 'password'}),
    Request(requests.put, 'user', {'nick': 'ala2',
                            'email': 'xd@test.com', 'password': 'password'}),
    Request(requests.put, 'user', {'nick': 'ala3',
                            'email': 'xdd@test.com', 'password': 'password'}),
    Request(requests.put, 'user', {'nick': 'ala2',
                            'email': 'xdtest.com', 'password': 'password'}),

    Request(requests.get, 'user', {'id': 1}),
    Request(requests.get, 'user', {'id': 2}),
    Request(requests.get, 'user', {'id': 3}),

    Request(requests.get, 'user/data', {'id': 3}),
    Request(requests.put, 'user/data', {'id': 3, 'json': {'data': 'otherdata'}}),
    Request(requests.get, 'user/data', {'id': 3}),

    Request(requests.patch, 'user', {'id': 3, 'field': 'nick', 'value': 'patched1'}),
    Request(requests.patch, 'user', {'id': 3, 'field': 'nick', 'value': 'patched2'}),
    Request(requests.patch, 'user', {'id': 3, 'field': 'nick', 'value': 'patched3'}),

    Request(requests.get, 'user', {'id': 3}),


    Request(requests.delete, 'user', {'id': 1}),
    Request(requests.delete, 'user', {'id': 2}),
    Request(requests.delete, 'user', {'id': 3}),
    Request(requests.delete, 'user', {'id': 4}),
)

with open('tests/test_results.html', 'w') as file:
    file.write(template.render(title=str(datetime.now()), reqs=reqs))
