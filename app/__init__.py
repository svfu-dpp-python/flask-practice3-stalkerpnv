from flask import Flask

from app import views
from app.database import db, migrate


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
    db.init_app(app)
    migrate.init_app(app, db)

    app.add_url_rule("/", view_func=views.index_page)
    app.add_url_rule("/book_list/", view_func=views.book_list)
    app.add_url_rule("/book_new/", view_func=views.book_edit, methods=["GET", "POST"])
    app.add_url_rule("/book_delete/<int:pk>/", view_func=views.book_delete, methods=["GET", "POST"])
    app.add_url_rule("/book_edit/<int:pk>/", view_func=views.book_edit, methods=["GET", "POST"])
    return app
