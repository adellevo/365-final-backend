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

wallet = Blueprint('wallet', __name__)
@wallet.route('/addwallet', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
@jwt_required()
def add_wallets():
    data = request.json
    # --- add to wallet table ---
    # walletId = data["walletId"]
    address = data["address"]
    privateKey = data["privateKey"]
    name = data["name"]

    # get user
    userId = get_jwt_identity()
    user = User.query.filter_by(userId=userId).first() 
    userId = user.userId

    new_wallet = Wallet(address=address, privateKey=privateKey,name=name, userId=userId)
    db.session.add(new_wallet)
    
    db.session.commit()
    return jsonify({"walletId": new_wallet.walletId, "address": address,"privateKey": privateKey, "userId": userId}), 200



@wallet.route('/remove-wallet', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
@jwt_required()
def add_wallet():
    data = request.json
    # --- add to wallet table ---
    # walletId = data["walletId"]
    address = data["address"]
    name = data["name"]

    # get user
    userId = get_jwt_identity()
    user = User.query.filter_by(userId=userId).first() 
    userId = user.userId

    new_wallet = Wallet(address=address, privateKey=privateKey,name=name, userId=userId)
    db.session.add(new_wallet)
    
    db.session.commit()
    return jsonify({"walletId": new_wallet.walletId, "address": address,"privateKey": privateKey, "userId": userId}), 200

