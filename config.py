import os


basedir = os.path.abspath(os.path.dirname(__file__))

config = {
    'DEBUG': True,
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,

    'SECRET_KEY': os.environ.get('SECRET_KEY', 'testkey'),
    'JWT_SECRET_KEY': os.environ.get('JWT_SECRET_KEY', 'testkey'),

    'JSONIFY_PRETTYPRINT_REGULAR': True,

    'SQLALCHEMY_DATABASE_URI': f'sqlite:///{os.path.join(basedir, "db/database.db")}',
    'DB_FILE_URL': os.path.join(basedir, "db/database.db"),
    'USER_JSON_PATH': os.path.join(basedir, 'db/user_data/'),
    'RESPONSE_JSON_PATH': os.path.join(basedir, 'db/responses/')
}
