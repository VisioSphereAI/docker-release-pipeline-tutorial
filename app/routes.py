from datetime import datetime

from flask import Blueprint, jsonify, request, render_template, current_app, redirect, url_for
from werkzeug.exceptions import BadRequest

from .calendar_manager import EventCalendar
from .task_manager import TaskManager

main_bp = Blueprint("main", __name__)

# Initialize managers
event_calendar = EventCalendar()
task_manager = TaskManager()

# Pre-populate sample events and tasks
event_calendar.add_event("2026-04-11", "Team Meeting")
event_calendar.add_event("2026-04-12", "Project Deadline")
event_calendar.add_event("2026-04-15", "Conference")
task_manager.add_task("Build Flask Docker app", "Create a sample Flask app with Docker support", "high")
task_manager.add_task("Add calendar feature", "Implement event calendar", "medium")
task_manager.add_task("Write documentation", "Complete API and setup docs", "medium")
task_manager.add_task("Add tests", "Increase test coverage", "low")


def _template_context():
    return {
        "project_name": current_app.config.get("PROJECT_NAME", "Flask Docker Sample"),
        "current_year": datetime.utcnow().year,
    }


@main_bp.route("/", methods=["GET"])
def home():
    context = _template_context()
    context["title"] = "Home"
    return render_template("home.html", **context)


@main_bp.route("/about", methods=["GET"])
def about():
    context = _template_context()
    context["title"] = "About"
    return render_template("about.html", **context)


@main_bp.route("/contact", methods=["GET"])
def contact():
    context = _template_context()
    context["title"] = "Contact"
    return render_template("contact.html", **context)


@main_bp.route("/api/v1/echo", methods=["POST"])
def echo():
    payload = request.get_json(silent=True)
    if not payload or "message" not in payload:
        raise BadRequest("Request JSON must include a 'message' field.")

    return jsonify({"echo": payload["message"]}), 201


@main_bp.route("/calendar", methods=["GET"])
def calendar():
    """Display interactive calendar."""
    context = _template_context()
    context["title"] = "Calendar"

    year, month = EventCalendar.get_months_years()
    context["calendar_data"] = event_calendar.get_calendar_data(year, month)
    context["year"] = year
    context["month"] = month
    context["month_name"] = EventCalendar.get_month_name(month)

    # Get previous and next month for navigation
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1

    context["prev_url"] = f"?year={prev_year}&month={prev_month}"
    context["next_url"] = f"?year={next_year}&month={next_month}"

    return render_template("calendar.html", **context)


@main_bp.route("/tasks", methods=["GET", "POST"])
def tasks():
    """Display and manage tasks."""
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description", "")
        priority = request.form.get("priority", "medium")

        if title:
            task_manager.add_task(title, description, priority)

        return redirect(url_for("main.tasks"))

    context = _template_context()
    context["title"] = "Tasks"
    context["tasks"] = task_manager.get_all_tasks()
    context["stats"] = task_manager.get_stats()

    return render_template("tasks.html", **context)


@main_bp.route("/tasks/<int:task_id>/toggle", methods=["POST"])
def toggle_task(task_id):
    """Toggle task completion status."""
    task = task_manager.get_task(task_id)
    if task:
        task_manager.update_task(task_id, completed=not task["completed"])

    return redirect(url_for("main.tasks"))


@main_bp.route("/tasks/<int:task_id>/delete", methods=["POST"])
def delete_task(task_id):
    """Delete a task."""
    task_manager.delete_task(task_id)
    return redirect(url_for("main.tasks"))
