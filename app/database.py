from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()


class Book(db.Model):
    pk = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(75), nullable=False)
    author = db.Column(db.Integer, db.ForeignKey("author.pk", name="author"))

    def __str__(self):
        return f"{self.name}"


class Author(db.Model):
    pk = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(25), nullable=False)
    first_name = db.Column(db.String(25), nullable=False)
    second_name = db.Column(db.String(25))

    def __str__(self):
        return f"{self.last_name} {self.first_name:.1}."
