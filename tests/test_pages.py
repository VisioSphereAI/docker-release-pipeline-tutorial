from app import create_app


def test_home_page():
    app = create_app("app.config.TestingConfig")
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"Welcome to Flask Docker" in response.data
    assert b"Calendar" in response.data
    assert b"Task Manager" in response.data


def test_calendar_page():
    app = create_app("app.config.TestingConfig")
    client = app.test_client()

    response = client.get("/calendar")

    assert response.status_code == 200
    assert b"Event Calendar" in response.data


def test_tasks_page():
    app = create_app("app.config.TestingConfig")
    client = app.test_client()

    response = client.get("/tasks")

    assert response.status_code == 200
    assert b"Task Manager" in response.data


def test_add_task():
    app = create_app("app.config.TestingConfig")
    client = app.test_client()

    response = client.post("/tasks", data={
        "title": "Test Task",
        "description": "A test task",
        "priority": "high",
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Test Task" in response.data


def test_about_page():
    app = create_app("app.config.TestingConfig")
    client = app.test_client()

    response = client.get("/about")

    assert response.status_code == 200
    assert b"About This Project" in response.data


def test_contact_page():
    app = create_app("app.config.TestingConfig")
    client = app.test_client()

    response = client.get("/contact")

    assert response.status_code == 200
    assert b"Get In Touch" in response.data
