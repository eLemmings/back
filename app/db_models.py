# Modele tabel do ORM
from app import db
from flask_bcrypt import check_password_hash, generate_password_hash


class Users(db.Model):
    # Model tabeli użytkowników
    id = db.Column(
        db.Integer,
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
    shares = db.relationship('Shares', backref='user')

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf-8')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'User:\n {self.id}\n {self.email}\n {self.nick}\n'


class Shares(db.Model):
    # Model dzienników udostępnionych
    uuid = db.Column(
        db.String(32),
        primary_key=True)
    diary_index = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id), nullable=False)

    def __repr__(self):
        return f'Share:\n {self.uuid}\n {self.diary_index}\n {self.user_id}\n'