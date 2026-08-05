"""Main application package — Flask app factory."""

from flask import Flask, render_template, request

from libera import auth, core
from libera.database import db
from libera.extensions import init_cors
from libera.settings import config


def create_app(config_object=config):
    """Application factory."""
    app = Flask(__name__)
    app.config.from_object(config_object)

    # -- Database ------------------------------------------------------------
    db.init_app(app)
    db.create_all()

    # -- Logging -------------------------------------------------------------
    app.logger.info("Using %s", config_object.__class__.__name__)
    app.logger.info("Debug mode: %s", config_object.DEBUG)
    app.logger.info("DB_URI: %s", app.config["DB_URI"])

    # -- Extensions & blueprints ---------------------------------------------
    register_extensions(app)
    register_blueprints(app)
    register_error_handlers(app)
    register_context_processors(app)

    return app


def register_extensions(app: Flask):
    """Register Flask extensions (CORS, etc.)."""
    init_cors(app)


def register_blueprints(app: Flask):
    """Register application blueprints."""
    app.register_blueprint(core.views.blueprint)
    app.register_blueprint(auth.views.blueprint)


def register_context_processors(app: Flask):
    """Inject template-global variables."""

    @app.context_processor
    def inject_current_user():
        from libera.auth.func import get_userdata_from_session

        session_id = request.cookies.get("session")
        if session_id:
            user = get_userdata_from_session(session_id)
            return {"current_user": user}
        return {"current_user": None}


def register_error_handlers(app: Flask):
    """Register HTTP error handlers."""

    @app.errorhandler(404)
    def not_found(_e):
        return (
            render_template(
                "handlers/handler.html",
                error_code="404",
                error_message="Page Not Found",
            ),
            404,
        )

    @app.errorhandler(405)
    def method_not_allowed(_e):
        return (
            render_template(
                "handlers/handler.html",
                error_code="405",
                error_message="Method Not Allowed",
            ),
            405,
        )

    @app.errorhandler(500)
    def internal_server_error(_e):
        return (
            render_template(
                "handlers/handler.html",
                error_code="500",
                error_message="Internal Server Error",
            ),
            500,
        )
