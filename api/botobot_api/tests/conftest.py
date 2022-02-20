import pytest

from botobot_api.app import create_app
from botobot_api.ext.commands import create_db, drop_db

@pytest.fixture(scope="session")
def app():
    app = create_app()
    with app.app_context():
        create_db()
        yield app
        drop_db()

@pytest.fixture()
def client(app):
    return app.test_client()
