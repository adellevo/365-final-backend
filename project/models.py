from flask_login import UserMixin
from . import db
from flask_sqlalchemy import SQLAlchemy

class User(UserMixin, db.Model):
    def get_id(self):
           return (self.userId)

    userId = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

class Wallet(db.Model):
    def get_id(self):
           return (self.walletId)

    walletId = db.Column(db.Integer, primary_key=True) 
    address = db.Column(db.String(50), unique=True)
    privateKey = db.Column(db.String(50), unique=True)
    userId = db.Column(db.Integer, unique=True)

    