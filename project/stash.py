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

stash = Blueprint('stash', __name__)

@stash.route('/create-stash', methods=['POST'])
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
    new_stash = Stash(name=data['name'], userId=current_user,walletId=data['walletId'])
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


@stash.route('/delete-stash', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
@jwt_required()
def delete_stash():
    data = request.json
    stash = Stash.query.filter_by(stashId=data['stashId'])
    stash_txs = Transaction.query.filter_by(stashId=data['stashId'])
    for tx in stash_txs:
        tx.delete()
        tx_events = Event.query.filter_by(transactionId=tx.transactionId)
        for event in tx_events:
            event.delete()
        tx_args = Arg.query.filter_by(transactionId=tx.transactionId)
        for arg in tx_args:
            arg.delete()
    if stash:
        stash.delete()
        db.session.commit()
        return {"message":"Stash Delete"},200
    else:
        return {"message":"No Stash found by ID"},400

@stash.route('/insert-transaction', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
@jwt_required()
def insert_transaction():
    data = request.json
    tx = data['transaction']
    events = tx['events']
    new_txn = Transaction(address=tx['address'], module= tx['module'], function=tx['function'],
             date= tx['date'],transactionId=tx['hash'],stashId=data['stashId'])
    for event in events:
        new_event = Event(eventType=event['type'], name=event['name'], amount=event['amount'], transactionId=tx['hash'])
        db.session.add(new_event)
        for i in range(len(tx['args'])):
            arg = tx['args']
            new_arg = Arg(genericType=arg['genericType'], value=arg['value'], transactionId=tx['hash'],index=i)
            db.session.add(new_arg)
   
    db.session.add(new_txn)
    db.session.commit()

# LOOK for stashes with addr/func/event
@stash.route('/stash-contains')
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
@jwt_required()
def stash_contains():

    pass


# Look for txs with addr/func/event





