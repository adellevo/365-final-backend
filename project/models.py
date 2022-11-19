from . import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, Table
# from flaskl_sqlalchemy import SQLAlchemy.
# https://prod.liveshare.vsengsaas.visualstudio.com/join?7174E3856CBFA5BD076070B8632B16F383B0
# 0xdfc873cf7dc8bc99148f0704574dee49b322e7558337315a53f5b9b2758d24ea
class User(db.Model):
    def get_id(self):
           return (self.userId)

    userId = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def get_user(self):
        return {
            "userId": self.userId,
            "username": self.username,
            "password": self.password,

        }

class Wallet(db.Model):
    def get_id(self):
           return (self.walletId)

    walletId = db.Column(db.Integer, primary_key=True) 
    userId = db.Column(db.Integer)
    name=db.Column(db.String(100),nullable=True)
    address = db.Column(db.String(66), unique=False)
    privateKey = db.Column(db.String(50), unique=False,nullable=True)

class Stash(db.Model):
    def get_id(self):
           return (self.stashId)

    stashId = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(66))
    userId = db.Column(db.Integer)
    walletId = db.Column(db.Integer)

    def get_stash(self):
        return {
            "stashId": self.stashId,
            "name": self.name,
            "userId": self.userId,
            "walletId": self.walletId,
        }

class Transaction(db.Model):
       def get_id(self):
           return (self.transactionId)
           
       transactionId = db.Column(db.Integer, primary_key=True) 
       name = db.Column(db.String(66),nullable=True)
       address = db.Column(db.String(66))
       module = db.Column(db.String(100))
       function = db.Column(db.String(100))
       date = db.Column(db.String(100),nullable=True)
       stashId = db.Column(db.Integer)

       def get_transaction(self):
                 return {
                 "transactionId": self.transactionId,
                 "name": self.name,
                 "address": self.address,
                 "module": self.module,
                 "function": self.function,
              #    "date": self.date,
                 "stashId": self.stashId,
                 }
    #    userId = db.Column(db.Integer,db.ForeignKey("user.userId"))
    

class Event(db.Model):
       def get_id(self):
              return (self.eventId)
       eventId = db.Column(db.Integer, primary_key=True)
       eventType = db.Column(db.String(50))
       name = db.Column(db.String(50))
       amount = db.Column(db.Integer,nullable=True)
       transactionId = db.Column(db.Integer)

class Arg(db.Model):
    def get_id(self):
           return (self.stashId)
    argId = db.Column(db.Integer, primary_key=True, unique=True)
    transactionId = db.Column(db.Integer)
    genericType = db.Column(db.String(50))
    index = db.Column(db.Integer)
    value = db.Column(db.String(50))

