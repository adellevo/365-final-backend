# general imports
from flask import Blueprint, render_template, redirect, url_for, request, flash,jsonify

# cors + authentication
from flask_jwt_extended import create_access_token,jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import cross_origin

# sql execution
from . import db
from .models import *
import sqlalchemy
import urllib.parse

main = Blueprint('main', __name__)
# test
@main.route('/')
def index():
    return 200
    # return render_template('index.html')

@main.route('/profile')
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
@jwt_required()
def my_profile():
    current_user = get_jwt_identity()
    return jsonify(current_user), 200  

@main.route('/create-stash', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
@jwt_required()
def create_stash():
    #     "name": "stash name",
    #     "transactions": [
    #         {
    #             addr,module,function,date?,hash
    #             events: [
    #                 { type(eventType), amount} 
    #             ],
    #             args: [
        # {genericArg|null, value} -on insert argId,TxnId
    # ]
    # }
    data = request.json
    current_user = get_jwt_identity()
    new_stash = Stash(name=data['name'], userId=current_user['userId'],walletId=data['walletId'])
    db.session.add(new_stash)
    for tx in data['transactions']:
        events = tx['events']
        for event in events:
            new_event = Event(eventType=event['type'], name=event['name'], amount=event['amount'], transactionId=tx['hash'])
            db.session.add(new_event)
        for i in range(len(tx['args'])):
            arg = tx['args']
            new_arg = Arg(genericType=arg['genericType'], value=arg['value'], transactionId=tx['hash'],index=i,)
            db.session.add(new_arg)
        new_txn = Transaction(address=tx['address'], module= tx['module'], function=tx['function'],
             date= tx['date'],transactionId=tx['hash'],stashId=new_stash.stashId)
        db.session.add(new_txn)
    
    db.session.commit()

@main.route('/add-wallet', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
@jwt_required()
def add_wallet():
    data = request.json

    # --- add to wallet table ---

    # walletId = data["walletId"]
    address = data["address"]
    privateKey = data["privateKey"]

    # get user
    userId = get_jwt_identity()
    user = User.query.filter_by(userId=userId).first() 
    userId = user.userId

    new_wallet = Wallet(address=address, privateKey=privateKey, userId=userId)
    db.session.add(new_wallet)

    # add to join table that links users and wallets
    # walletId = new_wallet.walletId
    # new_entry = UsersWallets(walletId=jsonify(walletId), userId=userId)
    # db.session.add(new_entry)
    
    db.session.commit()
    return jsonify({"walletId": new_wallet.walletId, "address": address,"privateKey": privateKey, "userId": userId}), 200

