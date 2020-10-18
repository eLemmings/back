# Moduł definiujący walidatory API

from marshmallow import Schema, fields, validate


class VUser(Schema):
    # Walidator rejestracji
    nick = fields.String(
        required=True, validate=validate.Length(min=4, max=30))
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


class VDiary(Schema):
    name=fields.String(required=True)
    type=fields.String(required=True, validate=validate.OneOf(['int', 'bool']))
    min=fields.Number()
    max=fields.Number()
    date=fields.Integer(required=True)
    colors=fields.List(fields.String(
        validate=validate.Regexp("#[0-9a-fA-F]{6}")))
    entries=fields.List(fields.List(fields.Number()))


class VJson(Schema):
    # Walidator danych JSON
    diaries = fields.List(fields.Nested(VDiary)) 