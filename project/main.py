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

