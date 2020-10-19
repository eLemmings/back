import os

from config import config as cf
from app import app

port = os.environ.get('PORT', 5000)

if __name__ == '__main__':
    app.run(debug=cf['DEBUG'], port=cf['PORT'])