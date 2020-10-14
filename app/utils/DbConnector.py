import os
import json
import shutil

from flask import jsonify

from config import config
from app.db_models import *

# TODO: Dokumentacja


class DbConnector:
    def __init__(self, db):
        self.db = db
        self.userProto = Users()  # User prototype

        if not os.path.exists(config['DB_FILE_URL']):
            print('No database detected')
            print('Creating database...')
            self.db.create_all()

    def gen_response(self, name: str) -> tuple:
        # Zwraca krotke z opisem odpowiedzi i jej kodem
        with open(config['RESPONSE_JSON_PATH'] + f'{name}.json') as file:
            res = json.load(file)

        return res, res['code']

    # ---

    def add_user(self, nick: str, email: str, password: str) -> None:
        # Dodaje użytkownika do bazy danych
        self.userProto.nick = nick
        self.userProto.email = email
        self.userProto.password = password

        self.db.session.add(self.userProto)
        self.db.session.flush()
        shutil.copy(config['USER_JSON_PATH'] + 'new.json',
                    config['USER_JSON_PATH'] + f'{self.userProto.id}.json')
        self.db.session.commit()

    def set_user_json(self, id: int, data: dict) -> None:
        # Aktualizuje dane JSON użytkownika
        with open(config['USER_JSON_PATH'] + f'{id}.json', 'w') as file:
            file.write(json.dumps(data))

    # ---

    def get_user(self, id: int) -> Users:
        # JSON z metadanymi użytkownika
        m = self.userProto.query.filter_by(id=id).first()
        return {'id': m.id, 'nick': m.nick, 'email': m.email}

    def get_user_data(self, id: int) -> tuple:
        # Wszystkie dane użytkownika
        meta = self.get_user(id)
        data = self.get_user_json(id)
        return {**meta, **data}

    def get_user_json(self, id: int) -> Users:
        # Słownik z danymi użytkownika
        with open(config['USER_JSON_PATH'] + f'{id}.json') as file:
            res = json.load(file)

        return res
