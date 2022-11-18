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
# @jwt_required()
def create_stash():
    data = request.json
    new_stash = Stash(name=data['name'], userId=2, walletId=data['walletId'])
    db.session.add(new_stash)
    db.session.commit()
    
    for tx in data['transactions']:
        new_txn = Transaction(address=tx['address'], function=tx['function'], stashId=new_stash.stashId)
        db.session.add(new_txn)
        db.session.commit()
        
        events = tx['events']
        for event in events:
            new_event = Event(eventType=event['type'], name=event['name'], amount=event['amount'], transactionId=new_txn.transactionId)
            db.session.add(new_event)
            db.session.commit()

    return {"message":"stash created"}, 200

@stash.route('/delete-stash', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
# @jwt_required()
def delete_stash():
    data = request.json
    stashId = data['stashId']
    stash = Stash.query.filter_by(stashId=stashId)
    stash_txs = Transaction.query.filter_by(stashId=stashId)
    
    for tx in stash_txs:
        tx_events = Event.query.filter_by(transactionId=tx.transactionId)
        for event in tx_events:
            Event.query.filter_by(eventId=event.eventId).delete()
            db.session.commit()

        Transaction.query.filter_by(transactionId=tx.transactionId).delete()
        db.session.commit()
       
    if stash:
        Stash.query.filter_by(stashId=stashId).delete()
        db.session.commit()
        return {"message":"Stash Delete"},200
    else:
        return {"message":"No Stash found by ID"},400

@stash.route('/insert-transaction', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
# @jwt_required()
def insert_transaction():
    data = request.json
    stashId = data['stashId']
    tx = data['transaction']

    new_txn = Transaction(address=tx['address'], function=tx['function'], stashId=stashId)
    db.session.add(new_txn)
    db.session.commit()
    
    events = tx['events']
    for event in events:
        new_event = Event(eventType=event['type'], name=event['name'], amount=event['amount'], transactionId=new_txn.transactionId)
        db.session.add(new_event)
        db.session.commit()

    return {"message":"transaction created"}, 200

# LOOK for stashes with addr/func/event
@stash.route('/stash-contains')
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
@jwt_required()
def stash_contains():

    pass


# Look for txs with addr/func/event





