import os

from app import config as cf
from app import app

port = os.environ.get('PORT', 5000)
app.run(debug=cf['DEBUG'])
