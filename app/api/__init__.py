from app import api
from app.api.resources import *


api.add_resource(User, '/user/<int:id>')
