import flask
import pytest 
import index

@pytest.fixture(name='app')
def setup_flask_app():
    """Configure a Flask app object to be used as a live server."""
    # configure index app
    index.app.config["TESTING"] = True
    yield index.app

@pytest.fixture(name="client")
def client_setup():
    # Configure Flask test server
    index.app.config["TESTING"] = True

    with index.app.test_client() as client:
        yield client