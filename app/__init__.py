from config import config

from flask_sqlalchemy import SQLAlchemy
from flask import Flask


app = Flask(__name__)

app.config.update(config)


db = SQLAlchemy(app)

from .test import test
from app import db_models

app.register_blueprint(test)
