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
    def __init__(self, method, endpoint: str, json: dict = None, token: str = None):
        self.func = method
        self.method = self.func.__name__.upper()
        self.endpoint = endpoint
        self.token = token
        self.params = json
        self.response = None
        self.text = self.call()

    def call(self):
        self.response = self.func(BASE+self.endpoint, json=self.params,
                                  headers={'Authorization': f'Bearer {self.token}'})
        try:
            return json.dumps(json.loads(self.response.text), indent=4)
        except:
            return self.response.text

    def get_params(self):
        return self.params

valid_json = {
    'diaries': [
        {
            'name': 'test',
            'type': 'int',
            'min': 1,
            'max': 5,
            'date': 12312315,
            'colors': ['#ffffff', '#000000', '#ff0000'],
            'entries': [[1,2,3,4], [2,3,4,1]]
        }
    ]
}

invalid_json = {
    'diaries': [
        {
            'type': 3,
            'min': 1,
            'max': 5,
            'date': 12312315,
            'colors': ['#fffff', '#000000', '#ff0000'],
            'entries': [3, [2,3,4,1]]
        }
    ]
}

register = Request(requests.post, 'register', {'nick': 'test_user',
                                        'email': 'test@test.com', 'password': 'password'})

token = Request(requests.post,
                'login', {'email': 'test@test.com', 'password': 'password'})


t = token.response.json().get('token', '')

share = Request(requests.put, 'share', {'index': 0}, token=t)

uuidres = Request(requests.get, 'share', token=t)

uuid = uuidres.response.json().get('shares')[0][0]

reqs = (
    register,
    token,
    share,
    uuidres,
    Request(requests.get, f'share/{uuid}'),

    Request(requests.get, 'user/data', token=t),
    Request(requests.put, 'user/data', valid_json, token=t),
    Request(requests.put, 'user/data', invalid_json, token=t),
    Request(requests.get, 'user/data', token=t),

    Request(requests.patch, 'user', {
            'field': 'nick', 'value': 'patched1'}, token=t),
    Request(requests.patch, 'user', {
            'field': 'nick', 'value': 'patched2'}, token=t),
    Request(requests.patch, 'user', {
            'field': 'nick', 'value': 'patched3'}, token=t),

    Request(requests.get, 'user', token=t),

    Request(requests.delete, 'user', token=t),
)

with open('tests/test_results.html', 'w') as file:
    file.write(template.render(title=str(datetime.now()), reqs=reqs))
