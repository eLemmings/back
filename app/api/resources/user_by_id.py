from flask_restful import Resource
from flask import jsonify, request

from app import db_connector


class UserById(Resource):
    # Zasób danych i metadanych użytkownika po id
    def get(self, id: int):
        return jsonify(db_connector.get_user_data(id))

    def delete(self, id: int):
        db_connector.delete_user(id)
        return db_connector.gen_response('ok')
