from config import config

from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask import Flask


app = Flask(__name__)

app.config.update(config)


db = SQLAlchemy(app)
api = Api(app)

from .test import test
from app import db_models
from app.api import *

app.register_blueprint(test)
