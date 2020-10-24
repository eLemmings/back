import os
import string, random


basedir = os.path.abspath(os.path.dirname(__file__))

# Generuje losowe klucze przy każdym uruchomieniu serwera
def random_key(n: int) -> str:
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=n))


# Konfiguracja serwera
config = {
    'DEBUG': os.environ.get('DEBUG', True),
    'PORT': os.environ.get('PORT', 5000),
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,

    'SECRET_KEY': random_key(50),
    'JWT_SECRET_KEY': random_key(50),

    'JSONIFY_PRETTYPRINT_REGULAR': True,

    'SQLALCHEMY_DATABASE_URI': f'sqlite:///{os.path.join(basedir, "db/database.db")}',
    'DB_FILE_URL': os.path.join(basedir, "db/database.db"),
    'USER_JSON_PATH': os.path.join(basedir, 'db/user_data/'),
    'RESPONSE_JSON_PATH': os.path.join(basedir, 'db/responses/')
}
