# Moduł definiujący endpointy API

from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify, request

import json as jsonlib
from marshmallow import ValidationError

from .validators import VUser, VUserPatch, VEmail, VJson, VDiaryIndex
from app import db_connector


class User(Resource):
    # /user/
    @jwt_required
    def get(self):
        # Zwraca wszystkie dane użytkownika
        return db_connector.get_user_data(get_jwt_identity())

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
        if js:=db_connector.get_user_json(get_jwt_identity()):
            return js
        return db_connector.gen_response('does_not_exist')

    @jwt_required
    def put(self):
        # Nadpisuje dane JSON użytkownika
        try:
            json = VJson().load(request.get_json())
            return db_connector.set_user_json(get_jwt_identity(), json)
        except ValidationError as error:
            return error.messages, 422


class UserShare(Resource):
    # /share
    @jwt_required
    def get(self):
        # Pobiera udostępnienia użytkownika
        if shares:=db_connector.get_user_shares(get_jwt_identity()):
            return shares, 200
        return db_connector.gen_response('does_not_exist')

    @jwt_required
    def put(self):
        # Tworzy link do udostępnienia
        try:
            index = VJson().load(request.get_json()['index'])
            return db_connector.create_share(get_jwt_identity(), index)
        except ValidationError as error:
            return error.messages, 422