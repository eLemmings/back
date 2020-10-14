from flask import Blueprint
from app.utils.DbConnector import DbConnector
from . import db

test = Blueprint('test', __name__)


@test.route('/', methods=['POST', 'GET'])
def main():
    x = DbConnector(db)
    return 'test'