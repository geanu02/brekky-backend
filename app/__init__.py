from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_login import LoginManager
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)
login = LoginManager(app)
CORS(app)

# CORS update

login.login_view = 'auth.signin'
login.login_message = "Login required"
login.login_message_category = "warning"

from app.blueprints.api import bp as api_bp
app.register_blueprint(api_bp)

from app import models 