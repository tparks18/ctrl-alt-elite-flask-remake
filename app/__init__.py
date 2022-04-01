from distutils.log import Log
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment


#init my login manager
login = LoginManager()
db = SQLAlchemy()
migrate = Migrate()
moment = Moment()

def create_app(config_class=Config):
    #link our config
    #init the app
    app = Flask(__name__)
    app.config.from_object(config_class)

    #register plugins
    login.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

#This is where you go if you are not logged in
    login.login_view='auth.login'
    login.login_message = 'Log yo punk ass into the website first'
    login.login_message_category = 'warning'

    moment.init_app(app)

    #do inits for database stuff

    from .blueprints.main import bp as main_bp
    app.register_blueprint(main_bp)

    from .blueprints.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from .blueprints.social import bp as social_bp
    app.register_blueprint(social_bp)

    from .blueprints.api import bp as api_bp
    app.register_blueprint(api_bp)

    return app

