from config import config

from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask import Flask



app = Flask(__name__)
CORS(app)

app.config.update(config)


api = Api(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


from app.utils import DbConnector

db_connector = DbConnector(db)

from app.api import *