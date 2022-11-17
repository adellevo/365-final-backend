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

# @main.route('/transactions', methods=['POST'])
# @cross_origin(origin='*',headers=['Content-Type','Authorization'])
# def filter_transactions():
#     data = request.json

#     eventType = 

