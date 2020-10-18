# Moduł definiujący endpointy API

from flask_restful import Resource
from flask import request

from app import db_connector


class Share(Resource):
    # /share/<string:uuid>
    def get(self, uuid: str):
        # Zwraca udostępniony dziennik
        res = db_connector.get_share(uuid)
        db_connector.delete_share(uuid)
        return res
