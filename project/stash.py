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
    new_stash = Stash(name=data['name'], userId=data['userId'], walletId=data['walletId'])
    db.session.add(new_stash)
    db.session.commit()
    
    for tx in data['transactions']:
        new_txn = Transaction(
            address=tx['address'],
            module = tx['module'],
            function=tx['function'],
            stashId=new_stash.stashId)
        db.session.add(new_txn)
        db.session.commit()
        
        # events = tx['events']
        # for event in events:
        #     new_event = Event(eventType=event['type'], name="DEFAULT", amount=1, transactionId=new_txn.transactionId)
        #     db.session.add(new_event)
        #     db.session.commit()

    return {"message":"stash created"}, 200

@stash.route('/user-stashes', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
@jwt_required()
def get_user_stashes():
    userId = get_jwt_identity()
    temp = []
    stashes = Stash.query.filter_by(userId=userId).all()
    for stash in stashes:
        temp_stash = stash.get_stash()
        # get all the transactions for each stash
        transactions = Transaction.query.filter_by(stashId=stash.stashId).all()
        temp_stash['transactions'] = []
        for transaction in transactions:
            temp_transaction = transaction.get_transaction()
            # get all the events for each transaction
            # events = Event.query.filter_by(transactionId=transaction.transactionId).all()
            # temp_transaction['events'] = []
            # for event in events:
            #     temp_transaction['events'].append(event.get_event())
            temp_stash['transactions'].append(temp_transaction)
        temp.append(temp_stash)
        print(stash.get_stash())
    return {"message":"Stashes found","stashes":temp}, 200


@stash.route('/delete-stash', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
# @jwt_required()
def delete_stash():
    data = request.json
    stash = Stash.query.filter_by(stashId=data['stashId'])
    stash_txs = Transaction.query.filter_by(stashId=data['stashId'])
    
    for tx in stash_txs:
        # tx.query.delete()
        tx_events = Event.query.filter_by(transactionId=tx.transactionId)
        for event in tx_events:
            event.query.delete()
            Event.delete().where(eventId=eventId)
            # db.session.commit()

        tx.query.delete()
        # db.session.commit()
       
    if stash:
        stash.query.delete()
        db.session.commit()
        return {"message":"Stash Delete"},200
    else:
        return {"message":"No Stash found by ID"},400

@stash.route('/insert-transaction', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
@jwt_required()
def insert_transaction():
    data = request.json
    stashId = data['stashId']
    tx = data['transaction']
    events = tx['events']
    print(events)
    
    new_txn = Transaction(address=tx['address'], function=tx['function'], stashId=stashId)
    db.session.add(new_txn)
    db.session.commit()
    
    for event in events:
        new_event = Event(eventType=event['type'], name=event['name'], amount=100000, transactionId=new_txn.transactionId)
        db.session.add(new_event)
        db.session.commit()

# LOOK for stashes with addr/func/event
@stash.route('/stash-contains')
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
@jwt_required()
def stash_contains():
    pass


# Look for txs with addr/func/event





