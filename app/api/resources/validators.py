# Moduł definiujący walidatory API

from marshmallow import Schema, fields, validate


class VUser(Schema):
    # Walidator rejestracji
    nick = fields.String(
        required=True, validate=validate.Length(min=4, max=30))
    email = fields.Email(required=True)
    password = fields.String(
        required=True, validate=validate.Length(min=8, max=30))


class VUserLogin(Schema):
    # Walidator logowania
    email = fields.Email(required=True)
    password = fields.String(
        required=True, validate=validate.Length(min=8, max=30))


class VEmail(Schema):
    # Walidator adresu email
    email = fields.Email(required=True)


class VUserPatch(Schema):
    # Walidator zapytania o zmianę pól w rekordzie użytkownika
    field = fields.String(required=True, validate=validate.OneOf(['nick']))
    value = fields.String(required=True)


class VEntry(Schema):
    # Walidator wpisu w dzienniku
    value = fields.Number(required=True)
    date = fields.Integer(required=True)
    description = fields.String()


class VDiary(Schema):
    # Walidator dziennika
    name = fields.String(required=True)
    min = fields.Number(required=True)
    max = fields.Number(required=True)
    color = fields.String(validate=validate.Regexp("#[0-9a-fA-F]{6}"))
    entries = fields.List(fields.Nested(VEntry), required=True)


class VJson(Schema):
    # Walidator danych JSON
    diaries = fields.List(fields.Nested(VDiary))


class VDiaryIndex(Schema):
    # Walidator indexu dziennika
    index = fields.Integer(required=True)
