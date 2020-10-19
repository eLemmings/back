import os

from config import config as cf
from app import app

if __name__ == '__main__':
    app.run(debug=cf['DEBUG'], port=cf['PORT'])