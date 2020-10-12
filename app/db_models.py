from . import db


class Users(db.Model):
    # Model tabeli użytkowników
    uuid = db.Column(
        db.int,
        primary_key=True)
    email = db.Column(
        db.String(100),
        unique=True,
        nullable=False)
    nick = db.Column(
        db.String(50),
        nullable=False)
    password = db.Column(
        db.String(100),
        nullable=False)

    def __repr__(self):
        return f'User:\n {self.uuid}\n {self.email}\n {self.nick}'

# TODO: Tabela udostępnionych zasobów np. dzienników wykresów itp
