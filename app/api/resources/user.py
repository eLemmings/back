# Moduł definiujący endpointy API

from flask_restful import Resource
from flask import jsonify, request

import json as jsonlib
from marshmallow import ValidationError

from .validators import VUser, VId, VUserPatch, VEmail, VJsonPatch, VJson
from app import db_connector


class User(Resource):
    # /user/
    def put(self):
        # Dodaje użytkownika - rejestracja
        try:
            user = VUser().load(request.get_json())
            return db_connector.add_user(user['nick'], user['email'], user['password'])
        except ValidationError as error:
            return error.messages, 422

    def get(self):
        # Zwraca dane użytkownika - id, nick
        try:
            id = VId().load(request.get_json())
            return db_connector.get_user(id['id'])
        except ValidationError as error:
            return error.messages, 422

    def delete(self):
        # Usuwa użytkownika
        try:
            id = VId().load(request.get_json())
            return db_connector.delete_user(id['id'])
        except ValidationError as error:
            return error.messages, 422

    def patch(self):
        # Pozwala na zmiane danych użytkownika - np nicku
        try:
            patch = VUserPatch().load(request.get_json())
            return db_connector.patch_user(patch['id'], patch['field'], patch['value'])
        except ValidationError as error:
            return error.messages, 422


class UserJSON(Resource):
    # /user/data
    def get(self):
        # Zwraca dane JSON użytkownika
        try:
            id = VId().load(request.get_json())
            return db_connector.get_user_json(id['id'])
        except ValidationError as error:
            return error.messages, 422

    def put(self):
        # Nadpisuje dane JSON użytkownika
        try:
            patch = VJsonPatch().load(request.get_json())
            json = VJson().load(patch['json'])
            return db_connector.set_user_json(patch['id'], json)
        except ValidationError as error:
            return error.messages, 422
