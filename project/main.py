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
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first() 
    userId = user.userId

    new_wallet = Wallet(address=address, privateKey=privateKey, userId=userId)
    db.session.add(new_wallet)

    # add to join table that links users and wallets
    walletId = new_wallet.walletId
    new_entry = UsersWallets(walletId=jsonify(walletId), userId=userId)
    db.session.add(new_entry)
    
    db.session.commit()
    return jsonify({"walletId": walletId, "address": address,"privateKey": privateKey, "userId": userId}), 200

