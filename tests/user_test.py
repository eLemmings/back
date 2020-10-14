import requests
import json
import os
from datetime import datetime

from jinja2 import Environment, FileSystemLoader


env = Environment(loader=FileSystemLoader('tests'))
template = env.get_template('test_template.html')

BASE = 'http://localhost:5000/'


class Request:
    def __init__(self, method: str, endpoint: str, params: dict = None):
        self.method = method
        self.endpoint = endpoint
        self.params = params
        self.response = None
        self.text = self.call()

    def call(self):
        self.response = requests.request(
            self.method, BASE+self.endpoint, data=self.params)
        try:
            return json.dumps(json.loads(self.response.text), indent=4)
        except:
            return self.response.text

    def get_params(self):
            return self.params


reqs = (
    Request('PUT', 'user', {'nick': 'kamil',
                              'email': 'kamil@test.com', 'password': 'password'}),
    Request('PUT', 'user', {'nick': 'alala',
                              'email': 'alala@test.com', 'password': 'password'}),
    Request('PUT', 'user', {'nick': 'ala2',
                              'email': 'xd@test.com', 'password': 'password'}),
    Request('GET', 'user/1'),
    Request('DELETE', 'user/1'),
    Request('GET', 'user'),
)

with open('tests/test_results.html', 'w') as file:
    file.write(template.render(title=str(datetime.now()), reqs=reqs))
