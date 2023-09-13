from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
DB_Name = "Grocery_Store.db"

def create_app():
    app = Flask(__name__,instance_relative_config=True)
    # app.config.from_pyfile('config.py')
    app.config['SECRET_KEY'] = 'My secret key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_Name}'
    db.init_app(app)

    from .api import apis
    from .auth import auth

    app.register_blueprint(apis, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')

    from .models import User

    login_manager = LoginManager()
    login_manager.login_view = 'auth.Login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    with app.app_context():
        db.create_all()

    return app