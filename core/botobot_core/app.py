from flask import Flask
from botobot_core.ext import configuration
from botobot_core.ext import resources

def create_app():
    """ Setups the app and add the resources. """
    app = Flask(__name__)
    configuration.init_app(app)
    resources.init_app(app)
    return app