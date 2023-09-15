from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "public_database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET KEY'] = '4ruB3$tG14l!*'
    app.secret_key = '4ruB3$tG14l!*'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    UPLOAD_FOLDER = 'website/static/'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    migrate = Migrate(app, db, render_as_batch=True)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/auth/")

    from .models import User, Game

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print("Created database!")
