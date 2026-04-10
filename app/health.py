from flask import Blueprint, jsonify, current_app

health_bp = Blueprint("health", __name__, url_prefix="/health")


@health_bp.route("/", methods=["GET"])
def health_check():
    return jsonify({
        "status": "ok",
        "environment": current_app.config.get("ENV", "production"),
        "project": current_app.config.get("PROJECT_NAME"),
    })
