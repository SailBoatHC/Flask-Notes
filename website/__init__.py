from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from sqlalchemy import create_engine

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'HEHEHAHA'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    #Migration PostgreSQL server connection: postgres://database_vz5w_user:rjp7fQdE08pjj63PXOEhB0eqYXG0RsNT@dpg-chtl0pt269vccp6q1cig-a.singapore-postgres.render.com/database_vz5w
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')

    from .models import User, Note

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('instance/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print("Created Database.")
