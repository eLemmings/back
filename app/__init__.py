from config import config

from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask import Flask



app = Flask(__name__)

app.config.update(config)


api = Api(app)
db = SQLAlchemy(app)

from .test import test
from app.utils import DbConnector

db_connector = DbConnector(db)

from app.api import *

app.register_blueprint(test)
