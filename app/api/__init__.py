from app import api
from app.api.resources import *


# Rejestracja endpointów
api.add_resource(UserJSON, '/user/data')
api.add_resource(User, '/user')
api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(Share, '/share/<string:uuid>')
api.add_resource(UserShare, '/share')
