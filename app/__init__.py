from flask import Flask

app = Flask(__name__)


from .test import test

app.register_blueprint(test)