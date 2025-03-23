from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
DB_NAME = 'database.sqlite3'

def create_database():
    db.create_all()
    print('Database Created')

def create_app():
    app = Flask(__name__)
    
    UPLOAD_FOLDER = 'website/static/uploads'
    GRAPHS_FOLDER = 'website/static/graphs'
    DATA_FOLDER = 'website/static/data'

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(GRAPHS_FOLDER, exist_ok=True)
    os.makedirs(DATA_FOLDER, exist_ok=True)

    app.config['SECRET_KEY'] = 'noslepums shush'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['GRAPHS_FOLDER'] = GRAPHS_FOLDER
    app.config['DATA_FOLDER'] = DATA_FOLDER

    db.init_app(app)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html')

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    from .views import views
    from .auth import auth
    from .models import User

    app.register_blueprint(views) 
    app.register_blueprint(auth, url_prefix='/') 


    with app.app_context():
        create_database()

    return app