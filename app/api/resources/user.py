from flask_restful import Resource


class User(Resource):
    # Zasób danych użytkownika
    def get(self, id: int):
        return 'user resource test'
