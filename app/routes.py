from datetime import datetime

from flask import Blueprint, jsonify, request, render_template, current_app
from werkzeug.exceptions import BadRequest

main_bp = Blueprint("main", __name__)


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
