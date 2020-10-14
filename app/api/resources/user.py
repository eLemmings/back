from flask_restful import Resource
from flask import jsonify, request

from app import db_connector


class User(Resource):
    # Zasób danych i metadanych użytkownika
    def put(self):
        f = request.form
        db_connector.add_user(f['nick'], f['email'], f['password'])
        return db_connector.gen_response('ok')
