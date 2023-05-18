from .extensions import db
from datetime import datetime
import string
from random import choices #this is used to generate random characters
from flask_login import UserMixin

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(2000))
    short_url = db.Column(db.String(7),unique=True)
    views = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.now)
    user = db.Column(db.Integer(), db.ForeignKey("user.id"))
    
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create short url
        self.short_url = self.generate_short_link()
        
    def generate_short_link(self):
        characters = string.digits + string.ascii_letters
        short_url = ''.join(choices(characters, k=7 ))
            
        # Check if link exist
        link = self.query.filter_by(short_url=short_url).first()
            
        if link:
            return self.generate_short_link()
        return short_url
        
        
        

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), unique=True, nullable=False)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    password = db.Column(db.String(length=60), nullable=False)
    link = db.relationship("Link", backref="user.link", lazy=True)