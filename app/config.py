import os


basedir = os.path.abspath(os.path.dirname(__file__))

config = {
    'DEBUG': True,
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,

    'SECRET_KEY': os.environ.get('SECRET_KEY', 'testkey'),

    'SQLALCHEMY_DATABASE_URI': f'sqlite:///{os.path.join(basedir, "db/database.db")}',
    'USER_JSON_URI': os.path.join(basedir, 'db/user_data.db')
}
