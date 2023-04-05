from flask import redirect, render_template, request, url_for

from app.database import Book, db


def index_page():
    return render_template("index.html")


def book_list():
    query = db.select(Book)
    books = db.session.execute(query).scalars()
    return render_template("book_list.html", books=books)


def book_edit(pk=None):
    book = db.get_or_404(Book, pk) if pk else Book()
    if request.method == 'POST':
        book.name = request.form["name"]
        if pk:
            book.verified = True
        else:
            db.session.add(book)
        db.session.commit()
        return redirect(url_for("book_list"))
    return render_template("book_edit.html", book=book)


def book_delete(pk):
    book = db.get_or_404(Book, pk)
    if request.method == 'POST':
        db.session.delete(book)
        db.session.commit()
        return redirect(url_for("book_list"))
    return render_template("book_delete.html", book=book)
