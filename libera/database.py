"""MySQL database connection and query helper for Flask applications."""

import mysql.connector
from flask import current_app, g


class DBConnector:
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        # Teardown: close connection after request
        app.teardown_appcontext(self.close_connection)

    def get_connection(self):
        if "db_conn" not in g:
            g.db_conn = mysql.connector.connect(
                host=current_app.config["DB_HOST"],
                user=current_app.config["DB_USER"],
                password=current_app.config["DB_PASSWORD"],
                database=current_app.config["DB_NAME"],
                port=current_app.config["DB_PORT"],
            )
        return g.db_conn

    def query(self, query, params=None, fetchone=False, fetchall=False):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(query, params or ())

        result = None
        if fetchone:
            result = cursor.fetchone()
        elif fetchall:
            result = cursor.fetchall()

        cursor.close()
        return result

    def insert(self, query, params=None):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(query, params or ())
        conn.commit()
        last_id = cursor.lastrowid

        cursor.close()
        return last_id

    def close_connection(self, exception=None):
        conn = g.pop("db_conn", None)
        if conn is not None:
            conn.close()


# database instance
db = DBConnector()
