import requests
import webbrowser
from pprint import pformat, pprint
from datetime import datetime
import json
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('tests'))
template = env.get_template('test_template.html')

BASE = 'http://localhost:5000/'

reqs = [
    ['PUT', requests.get(BASE + 'user/1', {'nick': 'josh',
                                        'email': 'josh@test.com', 'password': 'password'})],
    ['GET', requests.put(BASE + 'user/1')],
    ['GET', requests.put(BASE + 'user')],
]

with open(f'tests/results/user_test/{str(datetime.now())}.html', 'w') as file:
    for req in reqs:
        try:
            req.append(json.dumps(json.loads(req[1].text), indent=4))
        except:
            req.append(req[1].text)

    file.write(template.render(title=file.name, reqs=reqs))
    name = file.name
    file.close()

webbrowser.open(name)
exit()
