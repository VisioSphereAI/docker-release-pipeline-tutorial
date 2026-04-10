from flask import Flask

from .config import Config
from .errors import register_error_handlers
from .extensions import register_extensions
from .health import health_bp
from .routes import main_bp


def format_bytes(bytes_value):
    """Convert bytes to human readable format."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if bytes_value < 1024:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024
    return f"{bytes_value:.2f} PB"


def create_app(config_object=None):
    app = Flask(__name__, instance_relative_config=True)
    config_object = config_object or "app.config.Config"
    app.config.from_object(config_object)
    app.config.from_pyfile("config.py", silent=True)

    register_extensions(app)
    app.register_blueprint(main_bp)
    app.register_blueprint(health_bp)
    register_error_handlers(app)

    # Register custom Jinja2 filters
    app.jinja_env.filters["format_bytes"] = format_bytes

    return app
