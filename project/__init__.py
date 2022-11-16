from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import urllib.parse 
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_cors import CORS

import os
from dotenv import load_dotenv

load_dotenv()

escapedPassword = urllib.parse.quote_plus(os.environ.get("DB_PASSWORD"))
sqldialect = os.environ.get("DB_DIALECT")
username = os.environ.get("DB_USER")
database = os.environ.get("DB_NAME")
host = os.environ.get("DB_HOST")
key = os.environ.get("DB_SECRET_KEY")

# Build the connection string based on database specific parameters
connectionString = f"{sqldialect}://{username}:{escapedPassword}@{host}/{database}"

db = SQLAlchemy() 
app = Flask(__name__)
app.config['SECRET_KEY'] = key
app.config['SQLALCHEMY_DATABASE_URI'] = connectionString

jwt = JWTManager(app)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

db.init_app(app)

# blueprint for auth routes in our app
from .auth import auth as auth_blueprint
from .stash import stash as stash_blueprint
from .wallet import wallet as wallet_blueprint
app.register_blueprint(auth_blueprint)
app.register_blueprint(stash_blueprint)
app.register_blueprint(wallet_blueprint)

# blueprint for non-auth parts of app 
from .main import main as main_blueprint
app.register_blueprint(main_blueprint) 

from .models import User, Wallet

with app.app_context():
    user = User()
    wallet = Wallet()
    db.create_all()
