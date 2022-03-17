from distutils.log import Log
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

#init the app
app = Flask(__name__)
#link our config
app.config.from_object(Config)

#init my login manager
login = LoginManager(app)
#This is where you go if you are not logged in
login.login_view='login'
login.login_message = 'Log yo punk ass into the website first'
login.login_message_category = 'warning'

#do inits for database stuff
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from .blueprints.main import bp as main_bp
app.register_blueprint(main_bp)

from .blueprints.auth import bp as auth_bp
app.register_blueprint(auth_bp)

from app import models
