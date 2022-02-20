from flask import Flask
from botobot_api.ext import configuration
from botobot_api.ext import resources

# Setup the app.
def create_app():
    app = Flask(__name__)
    configuration.init_app(app)

    # Add resources.
    resources.init_app(app)
    return app