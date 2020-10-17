# Moduł definiujący endpointy API

from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify, request

import json as jsonlib
from marshmallow import ValidationError

from .validators import VUser, VUserPatch, VEmail, VJson
from app import db_connector


class User(Resource):
    # /user/
    @jwt_required
    def get(self):
        # Zwraca dane użytkownika - id, nick
        return db_connector.get_user(get_jwt_identity())

    @jwt_required
    def delete(self):
        # Usuwa użytkownika
        return db_connector.delete_user(get_jwt_identity())

    @jwt_required
    def patch(self):
        # Pozwala na zmiane danych użytkownika - np nicku
        try:
            patch = VUserPatch().load(request.get_json())
            return db_connector.patch_user(get_jwt_identity(), patch['field'], patch['value'])
        except ValidationError as error:
            return error.messages, 422


class UserJSON(Resource):
    # /user/data
    @jwt_required
    def get(self):
        # Zwraca dane JSON użytkownika
        return db_connector.get_user_json(get_jwt_identity())

    @jwt_required
    def put(self):
        # Nadpisuje dane JSON użytkownika
        try:
            json = VJson().load(request.get_json())
            return db_connector.set_user_json(get_jwt_identity(), json)
        except ValidationError as error:
            return error.messages, 422
