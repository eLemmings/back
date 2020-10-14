import os
import json
import shutil

from config import config
from app.db_models import Users

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

        return json.dumps(res), res['code']

    # ---

    def add_user(self, email: str, password: str, nick: str = '') -> tuple:
        # Dodaje użytkownika do bazy danych
        self.userProto.nick = nick
        self.userProto.email = email
        self.userProto.password = password

        try:
            self.db.session.add(self.userProto)
            self.db.session.flush()
            shutil.copy(config['USER_JSON_PATH'] + 'new.json',
                        config['USER_JSON_PATH'] + f'{self.userProto.id}.json')
            self.db.session.commit()
            self.gen_response('ok')
        except:
            self.gen_response('already_exist')

    def set_user_json(self, id: int, data: dict) -> tuple:
        # Aktualizuje dane JSON użytkownika
        with open(config['USER_JSON_PATH'] + f'{id}.json', 'w') as file:
            file.write(json.dumps(data))

        self.gen_response('ok')

    # ---

    def get_user(self, id: int) -> Users:
        # Obiekt ORM z metadanymi użytkownika
        return self.userProto.query.filter_by(id=id).first()

    def get_user_data(self, id: int) -> tuple:
        # Wszystkie dane użytkownika
        meta = self.userProto.query.filter_by(id=id).first()
        data = self.get_user_json(id)
        return meta, data

    def get_user_json(self, id: int) -> Users:
        # Plik JSON z danymi użytkownika
        with open(config['USER_JSON_PATH'] + f'{id}.json') as file:
            res = json.load(file)

        return res
