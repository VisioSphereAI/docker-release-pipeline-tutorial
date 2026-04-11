import pytest
from app import create_app


@pytest.fixture
def client():
    """A test client for the app."""
    app = create_app("app.config.TestingConfig")
    with app.test_client() as client:
        yield client


@pytest.fixture
def app():
    """An app instance."""
    app = create_app("app.config.TestingConfig")
    yield app