# Moduł definiujący walidatory API

from marshmallow import Schema, fields, validate


class VUser(Schema):
    # Walidator rejestracji
    nick = fields.String(
        required=True, validate=validate.Length(min=4, max=30))
    email = fields.Email(required=True)
    password = fields.String(
        required=True, validate=validate.Length(min=8, max=30))


class VId(Schema):
    # Walidator id
    id = fields.Integer(required=True)


class VEmail(Schema):
    # Walidator adresu email
    email = fields.Email(required=True)


class VUserPatch(VId):
    # Walidator zapytania o zmianę pól w rekordzie użytkownika
    field = fields.String(required=True, validate=validate.OneOf(['nick']))
    value = fields.String(required=True)


class VJsonPatch(VId):
    # Walidator danych JSON
    json = fields.String(required=True)


class VJson(Schema):
    # Walidator danych JSON
    data = fields.String(required=True)
