from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_assets import Environment, Bundle
from .util.assets import bundles

app = Flask(__name__)

assets = Environment(app)
assets.register(bundles)
app.config.from_object(Config)
app.config['ASSETS_DEBUG'] = False
app.config['ASSETS_VERSION'] = 'v1'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models