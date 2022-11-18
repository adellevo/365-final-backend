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

import json

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

# table populatation -- helper functions 

def populate_wallet_table(file_path):
    f = open(file_path)
    data = json.load(f)

    for wallet in data['wallets']:
        new_wallet = Wallet(userId=wallet['userId'], address=wallet['address'], privateKey=wallet['privateKey'])
        db.session.add(new_wallet)

    f.close()
    db.session.commit()

def populate_stash_table(file_path):
    f = open(file_path)
    data = json.load(f)

    start = 0
    end = 7000
    for i in range(start, end):
        stash = data['stashes'][i]
        new_stash = Stash(name=stash['name'], userId=stash['userId'], walletId=stash['walletId'])
        db.session.add(new_stash)

    f.close()
    db.session.commit() 

def populate_transaction_table(file_path):
    f = open(file_path)
    data = json.load(f)

    for transaction in data['transactions']:
        new_transaction = Transaction(address=transaction['address'], function=['function'], stashId=transaction['stashId'])
        db.session.add(new_transaction)
    
    f.close() 
    db.session.commit()

@main.route('/populate-db')
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def populate():
    # populate_wallet_table('/Users/adellevo/Desktop/CSC365/final-project/365-final-backend/project/data/wallets.json')
    populate_stash_table('/Users/adellevo/Desktop/CSC365/final-project/365-final-backend/project/data/stashes.json')
    # populate_transaction_table('/Users/adellevo/Desktop/CSC365/final-project/365-final-backend/project/transactions.json')
    return {"hello": "hi"}, 200  


# reporting query 1 - get count of each event type in stash
@main.route('/transactions/1', methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def reporting_1():
    data = request.json
    stashId = data['stashId']
    
    eventTypeData = db.session.query(Event.eventType, sqlalchemy.func.count(Event.eventType)).select_from(Event).\
        join(Transaction).\
        join(Stash).\
        filter_by(stashId=stashId).\
        group_by(Event.eventType)

    eventTypeCounts = []
    for event in eventTypeData:
        eventTypeCounts.append((event[0], event[1]))

    return {"eventTypeCounts": eventTypeCounts}, 200

# reporting query 2 - get all transactions associated with event type
@main.route('/transactions/2', methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def reporting_2():
    data = request.json
    stashId = data['stashId']
    eventType = data['eventType']

    events = Event.query.filter_by(eventType=eventType).join(Transaction).filter_by(stashId=stashId)

    transactionIds = []
    for event in events:
        transactionIds.append(event.transactionId)

    return {"transactionIds": transactionIds}, 200

# reporting query 3 - get all stashes associated with specific user
@main.route('/transactions/3', methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def reporting_3():
    data = request.json
    userId = data['userId']

    stashes = Stash.query.filter_by(userId=userId)

    stashIds = []
    for stash in stashes:
        stashIds.append(stash.stashId)

    return {"stashIds": stashIds}, 200

