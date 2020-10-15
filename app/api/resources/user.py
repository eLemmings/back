from flask_restful import Resource
from flask import jsonify, request

from app import db_connector


class User(Resource):
    # /user/
    def put(self):
        f = request.form
        return db_connector.add_user(f['nick'], f['email'], f['password'])

    def get(self):
        return db_connector.get_user_data(request.form['id'])

    def delete(self):
        return db_connector.delete_user(request.form['id'])

    def patch(self):
        f = request.form
        return db_connector.patch_user(f['id'], f['field'], f['value'])


class UserJSON(Resource):
    # /user/data/<int:id>/
    def patch(self, id: int):
        f = request.form
        return db_connector.patch_user(id, f)