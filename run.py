import os

from config import config as cf
from app import app

# Entry point aplikacji
if __name__ == '__main__':
    app.run(debug=cf['DEBUG'], port=cf['PORT'])