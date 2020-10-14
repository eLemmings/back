from app import api
from app.api.resources import *


api.add_resource(UserById, '/user/<int:id>')
api.add_resource(User, '/user')
# api.add_resource(UserMeta, '/user/meta/<int:id>')
# api.add_resource(UserData, '/user/data/<int:id>')
