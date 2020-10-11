import os

from config import config as cf
from app import *

port = os.environ.get('PORT', 5000)
app.run(debug=cf['debug'])