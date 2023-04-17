Website built for TFord Photo for ECT 471 database project.

Website is built in Flask and is using SQLAlchemy to cover the database. 

This uses flask-migrate to perform database migrations
    When new tables are added, use (venv) $ flask db migrate -m "table name i.e. 'users table'"
    Then, (venv) $ flask db upgrade


List of dependencies:

Package           Version
----------------- -------
alembic           1.10.3
click             8.1.3
Flask             2.2.3
Flask-Migrate     4.0.4
Flask-SQLAlchemy  3.0.3
Flask-WTF         1.1.1
greenlet          2.0.2
itsdangerous      2.1.2
Jinja2            3.1.2
Mako              1.2.4
MarkupSafe        2.1.2
pip               23.0.1
python-dotenv     1.0.0
setuptools        65.5.0
SQLAlchemy        2.0.9
typing_extensions 4.5.0
Werkzeug          2.2.3
WTForms           3.0.1
