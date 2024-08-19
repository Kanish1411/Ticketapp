from flask import Flask
from os import path
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME="database.db"

def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY'] = 'ugnqzabxzwrmkb'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    from views import views
    from auth import auth
    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')
    from models import User,Venue,Show
    login_manager = LoginManager()
    login_manager.login_view = 'auth.ulogin'   #redirect to login page if not logged in
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        user = User.query.filter_by(id=id).first()
        return user
    with app.app_context():
        create_db()

    return app

def create_db():
    if not path.exists('website/' + DB_NAME):
        db.create_all()
        print("Created Database")
