from flask import Flask

from app import views


def create_app():
    app = Flask(__name__)

    app.add_url_rule("/", view_func=views.index_page)

    return app