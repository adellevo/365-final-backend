from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User
import jsonify
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    data = request.json
    print("req ", data["username"])
    username = data["username"]
    password = data["password"]

    # user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database
    user = User.query.filter_by(username=username).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        return jsonify({"message": "Username already exists"}), 409

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    # new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
    new_user = User(username=username, password=generate_password_hash(password, method='sha256'))
    
    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    new_user["auth_token"] = create_access_token(identity = data["username"])
    return jsonify({"message": "User created successfully"}), 201

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/login', methods=['POST'])
def login_post():
    data = jsonify(request.json)
    username = data["username"]
    password = data["password"]
    remember = True if request.form.get('remember') else False
    user = User.query.filter_by(username=username).first()
    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid username or password"}), 401
    access_token = create_access_token(identity=username)
    user["access_token"] = access_token
    return jsonify(user)
