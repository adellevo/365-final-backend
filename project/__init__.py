import time
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import urllib.parse 
from flask_jwt_extended import JWTManager
from flask_cors import CORS

import os
from dotenv import load_dotenv
import sqlalchemy
from flask_apscheduler import APScheduler

from project.OracleClient import OracleClient

# set configuration values
class Config:
    SCHEDULER_API_ENABLED = True

load_dotenv()

escapedPassword = urllib.parse.quote_plus(os.environ.get("DB_PASSWORD"))
sqldialect = os.environ.get("DB_DIALECT")
username = os.environ.get("DB_USER")
database = os.environ.get("DB_NAME")
host = os.environ.get("DB_HOST")
key = os.environ.get("DB_SECRET_KEY")
  
# Build the connection string based on database specific parameters
# DATABASE_URL="mysql://myusername:mypassword@server.us-east-2.psdb.cloud/mydb?sslaccept=strict"

connectionString = f"{sqldialect}://{username}:{escapedPassword}@{host}/{database}?ssl_key=MyCertFolder/client-key.pem&ssl_cert=MyCertFolder/client-cert.pem"
sqlUrl = sqlalchemy.engine.url.URL(
    drivername="mysql+pymysql",
    username=username,
    password=escapedPassword,
    host=host,
    port=3306,
    database=database,
    query={"ssl_ca": "/etc/ssl/cert.pem"},
)
db = SQLAlchemy() 
app = Flask(__name__,)
app.config['SECRET_KEY'] = key
app.config['SSL'] = ('cert.pem', 'key.pem')
app.config['SQLALCHEMY_DATABASE_URI'] = sqlUrl
app.config['SCHEDULER_API_ENABLED'] = True
# initialize scheduler
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
jwt = JWTManager(app)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

db.init_app(app)

# blueprint for auth routes in our app
from .auth import auth as auth_blueprint
from .stash import stash as stash_blueprint
from .wallet import wallet as wallet_blueprint
from .dapp import dapp as dapp_blueprint
app.register_blueprint(auth_blueprint)
app.register_blueprint(stash_blueprint)
app.register_blueprint(wallet_blueprint)
app.register_blueprint(dapp_blueprint)

# blueprint for non-auth parts of app 
from .main import main as main_blueprint
app.register_blueprint(main_blueprint) 

# from .models import User, Wallet
from .models import *

# @scheduler.task('interval', id='do_job_1', seconds=5, misfire_grace_time=900)

# @scheduler.task('interval', id='oracle_manager', seconds=10, misfire_grace_time=900)
# def oracle_update():
#     with app.app_context():
#         print("Running oracle manager")
#         stopwatch = time.time()
        
#         new_prices = oc.update_switchboard()
#         for price in new_prices:
#             # print("PRICE",price)
#             o = Oracle(
#                 oracleName=price[0]+"_switchboard",
#                 price=price[1],
#                 timestamp=price[2])
#             # check if this oracle already exists
#             oracle = Oracle.query.filter_by(oracleName=o.oracleName, timestamp=price[2]).first()
#             if oracle is None:
#                 db.session.add(o)
#         db.session.commit()

with app.app_context():
    user = User()
    wallet = Wallet()
    # dapp = Dapp()
    db.create_all()
