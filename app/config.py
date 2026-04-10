from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-this-secret")
    DEBUG = False
    TESTING = False
    ENV = os.environ.get("FLASK_ENV", "production")
    JSONIFY_PRETTYPRINT_REGULAR = False
    PROJECT_NAME = "Flask Docker Sample"


class DevelopmentConfig(Config):
    DEBUG = True
    ENV = "development"


class TestingConfig(Config):
    TESTING = True
    ENV = "testing"


class ProductionConfig(Config):
    pass
