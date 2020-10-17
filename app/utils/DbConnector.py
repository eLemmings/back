'''
Moduł realizujący połączenie z bazą danych

Dane przechowywane są w formie rekordów oraz
w formie plików JSON wygodnych do przetwarzania w aplikacji
client side
'''

import os
import json
import shutil
from copy import copy

from flask import jsonify
from sqlalchemy import exc
from sqlalchemy.orm import exc as ormexc

from config import config
from app.db_models import *


class DbConnector:
    def __init__(self, db):
        self.db = db

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
        u = Users(nick=nick, email=email, password=password)

        try:
            self.db.session.add(u)
            self.db.session.commit()
            shutil.copy(config['USER_JSON_PATH'] + 'new.json',
                        config['USER_JSON_PATH'] + f'{u.id}.json')
            return self.gen_response('ok')
        except exc.IntegrityError:
            db.session.rollback()
            return self.gen_response('already_exist')

    def set_user_json(self, id: int, data: dict) -> None:
        # Aktualizuje dane JSON użytkownika
        with open(config['USER_JSON_PATH'] + f'{id}.json', 'w') as file:
            file.write(json.dumps(data))
        return self.gen_response('ok')

    def patch_user(self, id: int, field: str, value: str) -> dict:
        # Umożliwia aktualizacje pól rekordu użytkownika np nick albo hasło
        m = Users.query.filter_by(id=id).first()
        if not m:
            return self.gen_response('does_not_exist')
        if hasattr(m, field):
            setattr(m, field, value)
        else:
            db.session.rollback()
            return self.gen_response('bad_request')
        db.session.commit()
        return self.gen_response('ok')

    def delete_user(self, id: int) -> None:
        # Usuwa użytkownika
        try:
            m = Users.query.filter_by(id=id).first()
            self.db.session.delete(m)
            self.db.session.commit()
            os.remove(config['USER_JSON_PATH'] + f'{id}.json')
            return self.gen_response('ok')
        except ormexc.UnmappedInstanceError:
            self.db.session.rollback()
            return self.gen_response('does_not_exist')

    # ---

    def get_user(self, id: int) -> dict:
        # JSON z metadanymi użytkownika
        m = Users.query.filter_by(id=id).first()
        if not m:
            return {}
        return {'id': m.id, 'nick': m.nick}

    def get_user_data(self, id: int) -> tuple:
        # Wszystkie dane użytkownika
        meta = self.get_user(id)
        data = self.get_user_json(id)
        if meta and data:
            return {**meta, **data}
        return self.gen_response('does_not_exist')

    def get_user_json(self, id: int) -> dict:
        # Słownik z danymi użytkownika
        try:
            with open(config['USER_JSON_PATH'] + f'{id}.json') as file:
                res = json.load(file)
        except:
            return {}

        return res

    def check_user_exist(self, id: int) -> bool:
        # Sprawdza czy istnieje użytkownik o danym ID
        m = Users.query.filter_by(id=id).first()
        return bool(m)
