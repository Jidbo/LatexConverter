from flask import Flask
from flask import Blueprint
from flask_talisman import Talisman

main = Blueprint('main', __name__)

from . import routes

def create_app():

    app = Flask(__name__)
    # setup talisman
    csp = {
        'default-src': '\'self\'',
        'script-src': '\'self\'',
    }

    Talisman(app, strict_transport_security_include_subdomains=False,
             content_security_policy=csp)

    app.register_blueprint(main)

    return app
