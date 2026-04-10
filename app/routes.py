from datetime import datetime

from flask import Blueprint, jsonify, request, render_template, current_app, redirect, url_for, session
from werkzeug.exceptions import BadRequest

from .calendar_manager import EventCalendar
from .task_manager import TaskManager
from .gamification import GamificationManager
from .minigames import MiniGame
from .system_monitor import SystemMonitor

main_bp = Blueprint("main", __name__)

# Initialize managers
event_calendar = EventCalendar()
task_manager = TaskManager()
game_manager = GamificationManager()
mini_game = MiniGame()
system_monitor = SystemMonitor()

# Pre-populate sample events and tasks
event_calendar.add_event("2026-04-11", "Team Meeting")
event_calendar.add_event("2026-04-12", "Project Deadline")
event_calendar.add_event("2026-04-15", "Conference")
task_manager.add_task("Build Flask Docker app", "Create a sample Flask app with Docker support", "high")
task_manager.add_task("Add calendar feature", "Implement event calendar", "medium")
task_manager.add_task("Write documentation", "Complete API and setup docs", "medium")
task_manager.add_task("Add tests", "Increase test coverage", "low")


def _get_user_id():
    """Get or create user ID from session."""
    if "user_id" not in session:
        session["user_id"] = f"user_{id(session)}"
    return session["user_id"]


def _template_context():
    user_id = _get_user_id()
    user = game_manager.get_or_create_user(user_id)

    return {
        "project_name": current_app.config.get("PROJECT_NAME", "Flask Docker Sample"),
        "current_year": datetime.utcnow().year,
        "user": user,
        "user_id": user_id,
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
    user_id = _get_user_id()
    task = task_manager.get_task(task_id)
    if task and not task["completed"]:
        game_manager.increment_task_count(user_id)
    if task:
        task_manager.update_task(task_id, completed=not task["completed"])

    return redirect(url_for("main.tasks"))


@main_bp.route("/tasks/<int:task_id>/delete", methods=["POST"])
def delete_task(task_id):
    """Delete a task."""
    task_manager.delete_task(task_id)
    return redirect(url_for("main.tasks"))


@main_bp.route("/profile", methods=["GET", "POST"])
def profile():
    """User profile and gamification dashboard."""
    user_id = _get_user_id()

    if request.method == "POST":
        action = request.form.get("action")
        if action == "update_avatar":
            avatar = request.form.get("avatar", "🤖")
            game_manager.set_avatar(user_id, avatar)
        elif action == "update_username":
            username = request.form.get("username", f"Player_{user_id}")
            game_manager.set_username(user_id, username)

        return redirect(url_for("main.profile"))

    context = _template_context()
    context["title"] = "Profile"
    context["stats"] = game_manager.get_user_stats(user_id)
    context["avatars"] = ["🤖", "🚀", "🎮", "🧙", "🦸", "🧛", "🍕", "🌟", "👽", "🎯"]

    return render_template("profile.html", **context)


@main_bp.route("/leaderboard", methods=["GET"])
def leaderboard():
    """Global leaderboard."""
    context = _template_context()
    context["title"] = "Leaderboard"
    context["leaderboard"] = game_manager.get_leaderboard(20)

    return render_template("leaderboard.html", **context)


@main_bp.route("/games", methods=["GET"])
def games():
    """Mini-games hub."""
    context = _template_context()
    context["title"] = "Arcade"

    return render_template("games.html", **context)


@main_bp.route("/games/riddle", methods=["GET", "POST"])
def riddle_game():
    """Play riddle game."""
    user_id = _get_user_id()

    if request.method == "POST":
        answer = request.form.get("answer", "").strip().lower()
        riddle_answer = request.form.get("riddle_answer", "").strip().lower()

        if answer == riddle_answer:
            game_manager.add_points(user_id, 25, "riddle_solved")
            correct = True
        else:
            correct = False

        context = _template_context()
        context["title"] = "Riddle"
        context["riddle"] = mini_game.riddle()
        context["result"] = "correct" if correct else "incorrect"

        return render_template("riddle_game.html", **context)

    context = _template_context()
    context["title"] = "Riddle"
    context["riddle"] = mini_game.riddle()

    return render_template("riddle_game.html", **context)


@main_bp.route("/games/math", methods=["GET", "POST"])
def math_game():
    """Quick math challenge."""
    user_id = _get_user_id()

    if request.method == "POST":
        user_answer = request.form.get("answer", "").strip()
        correct_answer = request.form.get("correct_answer", "0")

        try:
            if int(user_answer) == int(correct_answer):
                game_manager.add_points(user_id, 15, "math_solved")
                correct = True
            else:
                correct = False
        except ValueError:
            correct = False

        context = _template_context()
        context["title"] = "Math Challenge"
        context["math"] = mini_game.quick_math()
        context["result"] = "correct" if correct else "incorrect"

        return render_template("math_game.html", **context)

    context = _template_context()
    context["title"] = "Math Challenge"
    context["math"] = mini_game.quick_math()

    return render_template("math_game.html", **context)


@main_bp.route("/system", methods=["GET"])
def system_monitor_page():
    """Display system performance monitoring."""
    context = _template_context()
    context["title"] = "System Monitor"
    
    system_info = system_monitor.get_all_info()
    context["system_info"] = system_info["system"]
    context["cpu_info"] = system_info["cpu"]
    context["memory_info"] = system_info["memory"]
    context["disk_info"] = system_info["disk"]
    context["network_info"] = system_info["network"]
    context["network_io"] = system_info["network_io"]
    context["battery_info"] = system_info["battery"]
    context["boot_time"] = system_info["boot_time"]
    context["processes"] = system_info["processes"]
    context["format_bytes"] = system_monitor.format_bytes
    
    return render_template("system_monitor.html", **context)


@main_bp.route("/api/v1/system/info", methods=["GET"])
def api_system_info():
    """API endpoint for system information."""
    return jsonify(system_monitor.get_all_info())


@main_bp.route("/api/v1/system/cpu", methods=["GET"])
def api_cpu_info():
    """API endpoint for CPU information."""
    return jsonify(system_monitor.get_cpu_info())


@main_bp.route("/api/v1/system/memory", methods=["GET"])
def api_memory_info():
    """API endpoint for memory information."""
    return jsonify(system_monitor.get_memory_info())


@main_bp.route("/api/v1/system/disk", methods=["GET"])
def api_disk_info():
    """API endpoint for disk information."""
    return jsonify(system_monitor.get_disk_info())


@main_bp.route("/api/v1/system/battery", methods=["GET"])
def api_battery_info():
    """API endpoint for battery information."""
    return jsonify(system_monitor.get_battery_info())


@main_bp.route("/api/v1/system/network", methods=["GET"])
def api_network_info():
    """API endpoint for network information."""
    network_data = system_monitor.get_network_info()
    return jsonify(network_data)
