"""Core views — home page (public) and thumbnail serving."""

import os

from flask import Blueprint, current_app, render_template, send_file
from flask.views import MethodView

from libera.utils import hyphenate_text

from .func import list_books

blueprint = Blueprint("core", __name__)


class IndexView(MethodView):
    """Public home page — lists all books.  No authentication required."""

    def get(self):
        context = {"message": "Fetched All books"}
        context["books"] = [
            {
                "id": book.id,
                "title": book.title,
                "summary": book.summary,
                "ISBN": book.ISBN,
                "genre": book.genre,
                "publication_year": book.publication_year,
                "author": book.author,
                "publisher": book.publisher,
                "rating": book.rating,
                "thumbnail": f"/book/thumbnail/{hyphenate_text(book.title)}.jpg",
            }
            for book in list_books()
        ]
        return render_template("index.html", **context)


@blueprint.route("/book/thumbnail/<filename>")
def serve_thumbnail(filename):
    path = os.path.join(current_app.config["APP_DIR"], f"assets/{filename}")
    return send_file(path, mimetype="image/jpg")


blueprint.add_url_rule("/", view_func=IndexView.as_view("home"))
