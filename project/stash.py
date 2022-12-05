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
        # print("SEM",new_txn.transactionId)
        
        events = tx['events']
        for event in events:
            print("EVENTS",event)
            new_event = Event(eventType=event['type'], name="DEFAULT", amount=1, transactionId=new_txn.transactionId)
            db.session.add(new_event)
        db.session.commit()

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
        print("stash: ", temp_stash)
        # get all the transactions for each stash
        transactions = Transaction.query.filter_by(stashId=stash.stashId).all()
        temp_stash['transactions'] = []
        for transaction in transactions:
            temp_transaction = transaction.get_transaction()
            print("transaction: ", temp_transaction)
            # get all the events for each transaction
            events = Event.query.filter_by(transactionId=transaction.transactionId).all()
            # print("events: ", [dict(e) for e in events])
            temp_transaction['events'] = []
            # for event in events:
            #     print(event.eventId)
            for event in events:
                print("event: ", event)
                temp_transaction['events'].append(event.get_event())
              
            temp_stash['transactions'].append(temp_transaction)
        temp.append(temp_stash)
        print(stash.get_stash())
    return {"message":"Stashes found","stashes":temp}, 200


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
@jwt_required()
def insert_transaction():
    data = request.json
    stashId = data['stashId']
    tx = data['transaction']
    events = tx['events']
    # print(events)
    
    new_txn = Transaction(address=tx['address'], function=tx['function'], stashId=stashId)
    db.session.add(new_txn)
    db.session.commit()
    
    for event in events:
        new_event = Event(eventType=event['type'], name=event['name'], amount=100000, transactionId=new_txn.transactionId)
        db.session.add(new_event)
    db.session.commit()








