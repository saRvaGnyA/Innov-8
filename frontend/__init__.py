from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from frontend.config import Config

# class UserInfo():
#     user_email=""
#     user_type=""

db = SQLAlchemy()
bcyrpt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()
# user_info = UserInfo()

def create_app(config_class = Config): 
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    bcyrpt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    # user_info.init_app(app)


    from frontend.users.routes import users
    from frontend.main.routes import main
    from frontend.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    return app




