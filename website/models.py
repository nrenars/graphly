from . import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, String

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(150))
    date_joined = db.Column(db.DateTime(), default=datetime.utcnow)
    
    graphs = db.relationship('Graph', backref='user', lazy=True)

    @property
    def password(self):
        raise AttributeError('Password is not a readable Attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password=password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password=password)

    def __str__(self):
        return f'<User {self.username}>'

class Graph(db.Model):
    __tablename__ = 'graph'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=True) 
    data = db.Column(db.String(1000), nullable=False) 
    color = db.Column(db.String(10), nullable=False) 
    graph_type = db.Column(db.String(50), nullable=False)
    graph_image = db.Column(db.String(1000), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
