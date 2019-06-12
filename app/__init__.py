from flask import Flask
from flask import Blueprint
from flask_talisman import Talisman
from flask_bootstrap import Bootstrap
from . import config

main = Blueprint('main', __name__)

from . import routes

def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(config.config[config_name])

    # setup Bootstrap
    Bootstrap(app)

    app.config['BOOTSTRAP_SERVE_LOCAL'] = True

    # setup talisman
    csp = {
        'default-src': '\'self\'',
        'script-src': ['\'self\'', '\'unsafe-eval\'']
    }

    Talisman(app, strict_transport_security_include_subdomains=False,
             content_security_policy=csp)

    app.register_blueprint(main)

    return app
