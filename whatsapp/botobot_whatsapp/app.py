from flask import Flask
from botobot_whatsapp.ext import configuration
from botobot_whatsapp.ext import resources

# Setup the app.
def create_app():
    app = Flask(__name__)
    configuration.init_app(app)

    # Add resources.
    resources.init_app(app)
    return app