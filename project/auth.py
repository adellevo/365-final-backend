# general imports
from flask import Blueprint, render_template, redirect, url_for, request, flash,jsonify

# cors + authentication
from flask_jwt_extended import create_access_token,jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import cross_origin

# sql execution
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def signup_post():
    # code to validate and add user to database goes here
    data = request.json
    username = data["username"]
    password = data["password"]

    # if this returns a user, then the email already exists in database
    user = User.query.filter_by(username=username).first() 
    
    # if a user is found, we want to redirect back to signup page so user can try again
    if user: 
        return {"message": "Username already exists"}, 409 

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(username=username, password=generate_password_hash(password, method='sha256'))
    
    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    user_dic = new_user.get_user()
    # user_dic["auth_token"] = create_access_token(identity = username)
    
    return jsonify({"user":user_dic,"message":"new account create"}), 201

@auth.route('/logout')
@jwt_required
def logout():
    # logout_user()
    return 200
    # return redirect(url_for('main.index'))

@auth.route('/login', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def login_post():
    data = request.json
    username = data["username"]
    password = data["password"]

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid username or password"}), 401
    
    user_dic = user.get_user()
    access_token = create_access_token(identity=username)
    user_dic["access_token"] = access_token
    return jsonify({"user":user_dic,"message":"Login success"})
