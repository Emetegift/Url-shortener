from flask import Flask
from .extensions import db
from .models import User, Link
from flask_login import LoginManager, login_user
from .routes import shortener

def create_app(config_file="settings.py"):
    app = Flask(__name__)
    
    app.config["SECRET_KEY"] = "secretkey"
    
    login_manager = LoginManager(app)
        
    
    
    app.config.from_pyfile(config_file)
    
    db.init_app(app)
    
    app.register_blueprint(shortener)
    
    return app
    
    #To create database
# from url_shortener import create_app
# from url_shortener.extensions import db
# from url_shortener.models import Link, User
# app = create_app()
# with app.app_context():
    # db.create_all()