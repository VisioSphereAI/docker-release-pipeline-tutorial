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

    # First add a task with a due date
    client.post("/calendar/add-task", data={
        "date": "2026-04-15",
        "title": "Calendar Task",
        "description": "Task added from calendar",
        "priority": "medium",
    })

    # Then check if calendar shows it
    response = client.get("/calendar")

    assert response.status_code == 200
    assert b"Calendar Task" in response.data


def test_tasks_page():
    app = create_app("app.config.TestingConfig")
    client = app.test_client()

    response = client.get("/tasks")

    assert response.status_code == 200
    assert b"Task Manager" in response.data


def test_add_task_from_calendar():
    app = create_app("app.config.TestingConfig")
    client = app.test_client()

    response = client.post("/calendar/add-task", data={
        "date": "2026-04-15",
        "title": "Calendar Task",
        "description": "Task added from calendar",
        "priority": "medium",
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Calendar Task" in response.data


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
