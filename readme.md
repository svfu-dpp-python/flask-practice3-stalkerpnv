# Flask-3

## Предварительные шаги

1. Откройте каталог проекта в редакторе VS Code

2. Создайте виртуальное окружение

3. Активируйте виртуальное окружение

4. Установите библиотеки `Flask`, `Flask-SqlAlchemy` и `Flask-Migrate`:

```powershell
pip install flask flask-migrate flask-sqlalchemy
```

5. Разрешите отладку:

Для включения отладки в Powershell:

```powershell
$ENV:FLASK_DEBUG=1
```

Для включения отладки в командной строке:

```cmd
set FLASK_DEBUG=1
```

## Создание проекта по шаблону Application Factory

1. В каталоге проекта, создайте каталог `app` а в нем подкаталог: `templates`

2. Создайте в каталоге app файл `__init__.py`:

```python
from flask import Flask

from app import views


def create_app():
    app = Flask(__name__)

    app.add_url_rule("/", view_func=views.index_page)

    return app
```

3. Создайте в каталоге `app` файл `views.py`:

```python
from flask import render_template


def index_page():
    return render_template("index.html")
```

4. Создайте в подкаталоге `templates` файл `base.html`:

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" crossorigin="anonymous">
    <title>Учебный сайт</title>
</head>
<body>
    <div class="container">
        <div class="row">
            <div class="col">
                {% block content %}{% endblock %}
            </div>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.bundle.min.js" crossorigin="anonymous"></script>
</body>
</html>
```

5. Создайте в подкаталоге `templates` файл `index.html`:

```html
{% extends "base.html" %}

{% block content %}
<h1>Добро пожаловать!</h1>
{% endblock %}
```

6. Запустите приложение и проверьте его работу в браузере:

```powershell
flask run
```

7. Сделайте коммит

## Добавление моделей SqlAlchemy

1. Создайте в каталоге `app` файл `database.py`:

```python
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()


class Book(db.Model):
    pk = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(75), nullable=False)

    def __str__(self):
        return f"{self.name}"
```

2. Добавьте в функцию `create_app()` сразу после создания объекта приложения `app`:

```python
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)
migrate.init_app(app, db)
```

а также соответствующий импорт:

```python
from app.database import db, migrate
```

3. Инициализируйте библиотеку Alembic (выполняется только один раз при инициализации проекта):

```powershell
flask db init
```

4. Выполните реструктуризацию базы данных (выполняется при каждой реструктуризации базы данных):

```powershell
flask db migrate
flask db upgrade
```

5. Скачайте, распакуйте приложение [Sqlite Browser](https://sqlitebrowser.org/dl/) и запустите его

6. Откройте файл базы данных `project.db` из каталоге `instance` в Sqlite Browser и проверьте структуру таблиц в базе данных

7. Сделайте скриншот, добавьте его в каталог проекта и сделайте коммит

## Добавление и чтение данных

1. Добавьте шаблон `book_list.html`:

```html
{% extends "base.html" %}

{% block content %}
<h1>Список книг</h1>
<ul>
    {% for b in books %}
    <li>{{ b }}</li>
    {% endfor %}
</ul>
<a href="{{ url_for('book_edit') }}">Создать книгу</a>
{% endblock %}
```

и шаблон `book_edit.html`:

```html
{% extends "base.html" %}

{% block content %}
<h1>Создание книги</h1>
<form method="post">
    <div class="mb-3">
        <label for="name" class="form-label">Название</label>
        <input type="text" name="name" id="name" class="form-control">
    </div>
    <input type="submit" value="Сохранить" class="btn btn-primary mb-3">
    <a href="{{ url_for('book_list') }}" class="btn btn-secondary mb-3">Отменить</a>
</form>
{% endblock %}
```

2. Добавьте в `views.py` функцию:

```python
def book_list():
    query = db.select(Book)
    books = db.session.execute(query).scalars()
    return render_template("book_list.html", books=books)
```

и функцию:

```python
def book_edit():
    book = Book()
    if request.method == 'POST':
        book.name = request.form["name"]
        db.session.add(book)
        db.session.commit()
        return redirect(url_for("book_list"))
    return render_template("book_edit.html")
```

3. Добавьте в шаблон `index.html` ссылку:

```html
<a href="{{ url_for('book_list') }}">Список книг</a>
```

Зарегистрируйте функции в `create_app()`:

```python
app.add_url_rule("/book_list/", view_func=views.book_list)
app.add_url_rule("/book_new/", view_func=views.book_edit, methods=["GET", "POST"])
```

4. Проверьте в браузере добавление и просмотр данных

5. Сделайте коммит

## Удаление данных

1. Добавьте шаблон `book_delete.html`:

```html
{% extends "base.html" %}

{% block content %}
<h1>Подтвердите удаление книги</h1>
<form method="post">
    <input type="hidden" name="pk" value="{{ book.pk }}">
    <div class="mb-3">
        <p>Название: {{ book.name }}</p>
    </div>
    <input type="submit" value="Удалить" class="btn btn-danger mb-3">
    <a href="{{ url_for('book_list') }}" class="btn btn-secondary mb-3">Отменить</a>
</form>
{% endblock %}
```

2. Добавьте в `views.py` функцию:

```python
def book_delete(pk):
    book = db.get_or_404(Book, pk)
    if request.method == 'POST':
        db.session.delete(book)
        db.session.commit()
        return redirect(url_for("book_list"))
    return render_template("book_delete.html", book=book)
```

3. Исправьте в шаблоне `book_list.html` список с книгами:

```html
<li>
    {{ b }}
    <a href="{{ url_for('book_delete', pk=b.pk) }}">
        <i class="bi bi-trash-fill"></i>
    </a>
</li>
```

Зарегистрируйте функцию в `create_app()`:

```python
app.add_url_rule("/book_delete/<int:pk>/", view_func=views.book_delete, methods=["GET", "POST"])
```

4. Проверьте в браузере удаление книг

5. Сделайте коммит

## Редактирование данных

1. Исправьте шаблон `book_edit.html`:

```html
{% extends "base.html" %}

{% block content %}
<h1>{% if book.pk %}Описание{% else %}Создание{% endif %} книги</h1>
<form method="post">
    <div class="mb-3">
        <input type="hidden" name="pk" value="{{ book.pk }}">
        <label for="name" class="form-label">Название</label>
        <input type="text" name="name" id="name" value="{% if book.name %}{{ book.name }}{% endif %}" class="form-control">
    </div>
    <input type="submit" value="Сохранить" class="btn btn-primary mb-3">
    <a href="{{ url_for('book_list') }}" class="btn btn-secondary mb-3">Отменить</a>
</form>
{% endblock %}
```

2. Исправьте в `views.py` функцию:

```python
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
```

3. Зарегистрируйте функцию в `create_app()`:

```python
app.add_url_rule("/book_edit/<int:pk>/", view_func=views.book_edit, methods=["GET", "POST"])
```

4. Проверьте в браузере редактирование книг

5. Сделайте коммит

## Ссылки

* [Документация Flask](https://flask.palletsprojects.com/)
* [Документация Flask-SqlAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
* [Документация Flask-Migrate](https://flask.palletsprojects.com/)
* [Документация SqlAlchemy](https://www.sqlalchemy.org/)
* [Документация Alembic](https://alembic.sqlalchemy.org/)
