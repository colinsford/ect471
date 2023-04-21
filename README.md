Website built for TFord Photo for ECT 471 database project.

Website is built in Flask and is using SQLAlchemy to cover the database. 

This uses flask-migrate to perform database migrations
    When new tables are added, use (venv) $ flask db migrate -m "table name i.e. 'users table'"
    Then, (venv) $ flask db upgrade

