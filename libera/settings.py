"""Application Configuration."""

import os
from .utils import generate_secret_key


class Config:
    """Base Configuration."""

    SECRET_KEY = os.environ.get("SECRET_KEY", generate_secret_key())
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    # File size restriction
    MAX_CONTENT_LENGTH = 24 * 1024 * 1024  # 24 megabytes
    # Database — prefer single DB_URI, fall back to individual vars
    _db_uri = os.environ.get("DB_URI", "")
    if _db_uri:
        from .utils import parse_db_uri

        _db = parse_db_uri(_db_uri)
        DB_HOST = _db["host"]
        DB_NAME = _db["name"]
        DB_USER = _db["user"]
        DB_PASSWORD = _db["password"]
        DB_PORT = _db["port"]
    else:
        DB_HOST = os.environ.get("DB_HOST")
        DB_NAME = os.environ.get("DB_NAME")
        DB_USER = os.environ.get("DB_USER")
        DB_PASSWORD = os.environ.get("DB_PASSWORD")
        DB_PORT = os.environ.get("DB_PORT")


class DevelopmentConfig(Config):
    """Development Configuration."""

    ENV = "dev"
    DEBUG = True


class ProductionConfig(Config):
    """Production Configuration."""

    ENV = "prod"
    DEBUG = False


class TestingConfig(Config):
    """Testing Configuration."""

    TESTING = True
    DEBUG = True


if os.environ.get("FLASK_ENV") == "production":
    config = ProductionConfig()
elif os.environ.get("FLASK_ENV") == "testing":
    config = TestingConfig()
else:
    config = DevelopmentConfig()
