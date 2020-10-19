# Moduł definiujący endpointy API

from flask_restful import Resource
from flask_jwt_extended import create_access_token
from flask import jsonify, request

import json as jsonlib
from marshmallow import ValidationError
import datetime

from .validators import VUser, VUserPatch, VEmail, VJson, VUserLogin
from app import db_connector


class Login(Resource):
    # /user/
    def post(self):
        try:
            cred = VUserLogin().load(request.get_json())
            user = db_connector.get_from_email(cred['email'])
        except ValidationError as error:
            return error.messages, 422

        if not user:
            return db_connector.gen_response('bad_email') # email invalid

        if not user.check_password(cred['password']):
            return db_connector.gen_response('bad_password') # password invalid

        token = create_access_token(identity=user.id, expires_delta=datetime.timedelta(days=30))
        return {'token': token}, 200


class Register(Resource):
    def post(self):
        # Dodaje użytkownika - rejestracja
        try:
            user = VUser().load(request.get_json())
            return db_connector.add_user(user['nick'], user['email'], user['password'])
        except ValidationError as error:
            return error.messages, 422
