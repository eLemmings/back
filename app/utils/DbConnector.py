'''
Moduł realizujący połączenie z bazą danych

Dane przechowywane są w formie rekordów oraz
w formie plików JSON wygodnych do przetwarzania w aplikacji
client side
'''

import os
import json
import shutil
import datetime
from copy import copy

from flask import jsonify
from sqlalchemy import exc
from sqlalchemy.orm import exc as ormexc

from config import config
from app.db_models import *
from .helpers import gen_pretty_id, gen_uuid


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

    def check_user_exist(self, id: int) -> bool:
        # Sprawdza czy istnieje użytkownik o danym ID
        m = Users.query.filter_by(id=id).first()
        return bool(m)

    # ---

    def add_user(self, nick: str, email: str, password: str) -> None:
        # Dodaje użytkownika do bazy danych
        u = Users(nick=nick, email=email, password=password)
        u.hash_password()

        try:
            self.db.session.add(u)
            self.db.session.commit()
            self.create_user_json(u.id)
            return self.gen_response('ok')
        except exc.IntegrityError:
            db.session.rollback()
            return self.gen_response('already_exist')

    def set_user_json(self, id: int, data: dict) -> None:
        # Aktualizuje dane JSON użytkownika
        with open(config['USER_JSON_PATH'] + f'{id}.json', 'w') as file:
            file.write(json.dumps(data))

        self.clear_shares(id)
        return self.gen_response('ok')

    def create_user_json(self, id: int) -> None:
        shutil.copy(config['USER_JSON_PATH'] + 'new.json',
                    config['USER_JSON_PATH'] + f'{id}.json')
        js = self.get_user_json(id)
        js['diaries'][0]['date'] = int(datetime.datetime.now().timestamp())
        self.set_user_json(id, js)

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


    # TODO: Zrobić coś z powtarzającym się kodem w poniższych funkcjach

    def delete_user(self, id: int) -> None:
        # Usuwa użytkownika
        try:
            user = Users.query.filter_by(id=id).first()
            if user.shares:
                self.db.session.delete(user.shares)
            self.db.session.delete(user)
            self.db.session.commit()
            os.remove(config['USER_JSON_PATH'] + f'{id}.json')
            return self.gen_response('ok')
        except ormexc.UnmappedInstanceError:
            self.db.session.rollback()
            return self.gen_response('does_not_exist')

    def create_share(self, id: int, index: int) -> dict:
        user = Users.query.filter_by(id=id).first()
        js = self.get_user_json(id)
        if not js or not js['diaries'][index]:
            return self.gen_response('bad_request')

        uuid = gen_uuid()
        share = Shares(uuid=uuid, diary_index=index, user=user)
        try:
            self.db.session.add(share)
            self.db.session.commit()
            return {'code': uuid}
        except exc.IntegrityError:
            db.session.rollback()
            return self.gen_response('already_exist')

    def delete_share(self, uuid: int) -> dict:
        share = Shares.query.filter_by(uuid=uuid).first()
        try:
            self.db.session.delete(share)
            self.db.session.commit()
            return self.gen_response('ok')
        except ormexc.UnmappedInstanceError:
            self.db.session.rollback()
            return self.gen_response('does_not_exist')

    def clear_shares(self, id: int) -> dict:
        user = Users.query.filter_by(id=id).first()
        try:
            self.db.session.delete(user.shares)
            self.db.session.commit()
            return self.gen_response('ok')
        except ormexc.UnmappedInstanceError:
            self.db.session.rollback()
            return self.gen_response('does_not_exist')

    # ---

    def get_user_shares(self, id: int) -> dict:
        shares = Shares.query.filter_by(user_id=id).all()
        if not shares:
            return {}

        res = {'shares': []}
        for share in shares:
            res['shares'].append([share.uuid, share.diary_index])

        return res

    def get_share(self, uuid: str):
        if not (share := Shares.query.filter_by(uuid=uuid).first()):
            return self.gen_response('does_not_exist')

        if not (js := self.get_user_json(share.user.id)):
            return self.gen_response('does_not_exist')

        try:
            res = js['diaries'][share.diary_index]
            res['nick'] = share.user.nick
            res['id'] = gen_pretty_id(share.user.id)
            return res, 200
        except:
            return self.gen_response('invalid_share')

    def get_user(self, id: int) -> dict:
        # JSON z metadanymi użytkownika
        user = Users.query.filter_by(id=id).first()
        if not user:
            return {}
        return {'id': user.id, 'pretty_id': gen_pretty_id(user.id), 'nick': user.nick}

    def get_from_email(self, email: str) -> dict:
        return Users.query.filter_by(email=email).first()

    def get_user_data(self, id: int) -> tuple:
        # Wszystkie dane użytkownika
        meta = self.get_user(id)
        data = self.get_user_json(id)
        shares = self.get_user_shares(id)
        if meta and data:
            return {**meta, **data, **shares}, 200
        return self.gen_response('does_not_exist')

    def get_user_json(self, id: int) -> dict:
        # Słownik z danymi użytkownika
        try:
            with open(config['USER_JSON_PATH'] + f'{id}.json') as file:
                res = json.load(file)
        except:
            return {}

        return res
