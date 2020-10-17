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


r = Request(requests.post, 'register', {'nick': 'test_user',
                                        'email': 'test@test.com', 'password': 'password'})

token = Request(requests.post,
                'login', {'email': 'test@test.com', 'password': 'password'})

t = token.response.json().get('token', '')


reqs = (
    r,
    token,
    Request(requests.get, 'user', token=t),

    Request(requests.get, 'user/data', token=t),
    Request(requests.put, 'user/data', {'data': 'otherdata'}, token=t),
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
