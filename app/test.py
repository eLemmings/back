from flask import Blueprint

test = Blueprint('test', __name__)

@test.route('/', methods=['POST', 'GET'])
def main():
    return 'test'