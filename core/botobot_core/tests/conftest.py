import pytest

from botobot_core.app import create_app
from botobot_core.ext.commands import create_db, drop_db

@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.testing = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
    with app.app_context():
        create_db()
        yield app
        drop_db()

@pytest.fixture()
def client(app):
    return app.test_client()
