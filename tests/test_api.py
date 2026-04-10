from app import create_app


def test_health_route():
    app = create_app("app.config.TestingConfig")
    client = app.test_client()

    response = client.get("/health/")

    assert response.status_code == 200
    assert response.json["status"] == "ok"
    assert response.json["environment"] == "testing"


def test_echo_route():
    app = create_app("app.config.TestingConfig")
    client = app.test_client()

    response = client.post("/api/v1/echo", json={"message": "hello"})

    assert response.status_code == 201
    assert response.json == {"echo": "hello"}


def test_echo_route_validation():
    app = create_app("app.config.TestingConfig")
    client = app.test_client()

    response = client.post("/api/v1/echo", json={})

    assert response.status_code == 400
    assert response.json["error"] == "bad_request"
