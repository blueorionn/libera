"""SQLAlchemy database session management for Flask."""

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class DB:
    """Thin wrapper around SQLAlchemy engine + scoped_session.

    Usage in the Flask app::

        db.init_app(app)          # call once during factory
        db.create_all()           # create tables if they don't exist
        db.session                # request-scoped session (use inside views)

    Usage in standalone scripts::

        db = DB(db_uri="mysql+pymysql://...")
        with db.session() as sess:
            ...
    """

    def __init__(self, app=None, db_uri=None):
        self.engine = None
        self._session_factory = None
        if app is not None:
            self.init_app(app)
        elif db_uri is not None:
            self.init_uri(db_uri)

    # -- Flask integration ---------------------------------------------------

    def init_app(self, app):
        """Wire up SQLAlchemy with a Flask application."""
        db_uri = app.config["DB_URI"]
        self._setup(db_uri)
        app.teardown_appcontext(self._close_session)

    def _setup(self, db_uri):
        self.engine = create_engine(db_uri, echo=False)
        self._session_factory = scoped_session(
            sessionmaker(bind=self.engine, autoflush=False, autocommit=False)
        )

    @property
    def session(self):
        """Return the current request-scoped session."""
        if self._session_factory is None:
            raise RuntimeError("DB.init_app() has not been called")
        return self._session_factory()

    def _close_session(self, exception=None):
        if self._session_factory is not None:
            self._session_factory.remove()

    # -- Standalone helper ---------------------------------------------------

    def init_uri(self, db_uri):
        """Initialise with just a URI (for scripts / tests)."""
        self._setup(db_uri)

    # -- Table creation ------------------------------------------------------

    def create_all(self):
        """Create all tables defined in :mod:`libera.models`."""
        from . import models  # noqa: F401  — ensure models are imported

        models.Base.metadata.create_all(self.engine)


# Singleton used by the Flask app.
db = DB()
