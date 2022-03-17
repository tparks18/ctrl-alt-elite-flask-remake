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

#do inits for database stuff
db = SQLAlchemy(app)
migrate = Migrate(app, db)
from app import routes, models
