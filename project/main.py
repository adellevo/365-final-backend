# general imports
from flask import Blueprint, render_template, redirect, url_for, request, flash,jsonify

# cors + authentication
from flask_jwt_extended import create_access_token,jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import cross_origin

# sql execution
from . import db
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
@jwt_required
def add_wallet():
    # add to wallet table

    # add to join table that links users and wallets
    wallet_to_add = UsersWallets(username=username, password=generate_password_hash(password, method='sha256'))
    db.session.add(wallet_to_add)
    
    db.session.commit()

