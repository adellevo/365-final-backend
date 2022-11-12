from flask_login import UserMixin
from . import db
from flask_sqlalchemy import SQLAlchemy

class User(UserMixin, db.Model):
    def get_id(self):
           return (self.userId)

    userId = db.Column(db.Integer, primary_key=True) 
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    