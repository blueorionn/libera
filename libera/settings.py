"""Application Configuration."""

import os
from urllib.parse import quote_plus

from .utils import generate_secret_key


class Config:
    """Base Configuration."""

    SECRET_KEY = os.environ.get("SECRET_KEY", generate_secret_key())
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    # File size restriction
    MAX_CONTENT_LENGTH = 24 * 1024 * 1024  # 24 megabytes

    S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")
    S3_BUCKET_URI = os.environ.get("S3_BUCKET_URI")

    # Database — single URI consumed directly by SQLAlchemy.
    #   MySQL:    mysql+pymysql://user:pass@host:port/dbname
    #   SQLite:   sqlite:///data.db
    _db_uri = os.environ.get("DB_URI", "")
    if not _db_uri:
        # Fall back to individual env vars (backward-compatible).
        _host = os.environ.get("DB_HOST", "")
        _port = os.environ.get("DB_PORT", "3306")
        _user = os.environ.get("DB_USER", "")
        _pass = os.environ.get("DB_PASSWORD", "")
        _name = os.environ.get("DB_NAME", "")
        if _user and _name and _host:
            _db_uri = (
                f"mysql+pymysql://{_user}:{quote_plus(_pass)}"
                f"@{_host}:{_port}/{_name}"
            )
        else:
            # Default: local SQLite in the project root.
            _db_uri = f"sqlite:///{os.path.join(PROJECT_ROOT, 'data.db')}"

    DB_URI = _db_uri


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
