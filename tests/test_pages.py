from app import create_app


def test_home_page():
    app = create_app("app.config.TestingConfig")
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"Welcome to the Flask multi-page site" in response.data


def test_about_page():
    app = create_app("app.config.TestingConfig")
    client = app.test_client()

    response = client.get("/about")

    assert response.status_code == 200
    assert b"About this project" in response.data


def test_contact_page():
    app = create_app("app.config.TestingConfig")
    client = app.test_client()

    response = client.get("/contact")

    assert response.status_code == 200
    assert b"Contact" in response.data
