from flask_login import UserMixin
from . import db
from flask_sqlalchemy import SQLAlchemy
# https://prod.liveshare.vsengsaas.visualstudio.com/join?7174E3856CBFA5BD076070B8632B16F383B0
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


# class Transaction(db.Model):
#        def get_id(self):
#            return (self.TransactionId)

#        transactionId = db.Column(db.Integer, primary_key=True) 
#        address = db.Column(db.String(64))
#        function = db.Column(db.String(100))
#        date = db.Column(db.Integer)
#        userId = db.Column(db.Integer)
#        payloadId = db.Column(db.Integer)
#        stashId = db.Column(db.Integer)
#        userId = db.Column(db.Integer)

# class Payload(db.Model):
#        def get_id(self):
#               return (self.PayloadId)
       


# class Event(db.Model):
#        def get_id(self):
#               return (self.eventId)
#        eventId = db.Column(db.Integer)
#        name = db.Column(db.String)
#        eventHandle = db.Column(db.String(64))
#        transactionId = db.Column(db.Integer)



class Wallet(db.Model):
    def get_id(self):
           return (self.walletId)

    walletId = db.Column(db.Integer, primary_key=True) 
    address = db.Column(db.String(50), unique=True)
    privateKey = db.Column(db.String(50), unique=True)
    userId = db.Column(db.Integer, unique=True)

# table that maps users to wallets
class UsersWallets(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    walletId = db.Column(db.Integer) 
    userId = db.Column(db.Integer) 

# class Stash(db.Model):
#     def get_id(self):
#            return (self.stashId)

#     stashId = db.Column(db.Integer, primary_key=True) 
#     privateKey = db.Column(db.String(64), unique=True)
#     userId = db.Column(db.Integer, unique=True)
#     walletId = db.Column(db.Integer, unique=True)

# class Parameter(db.Model):
#     def get_id(self):
#            return (self.stashId)

#     genericType = db.Column(db.String(50), unique=True)
#     name = db.Column(db.String(50), unique=True)
#     value = db.Column(db.String(50), unique=True)
#     parameterId = db.Column(db.Integer, unique=True)

