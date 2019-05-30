from flask import Flask
from flask import Blueprint

main = Blueprint('main', __name__)

from . import routes

def create_app():

    app = Flask(__name__)

    app.register_blueprint(main)

    return app
