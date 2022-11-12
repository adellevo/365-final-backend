from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import urllib.parse 
from flask_login import LoginManager

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
db.init_app(app)

# blueprint for auth routes in our app
from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app 
from .main import main as main_blueprint
app.register_blueprint(main_blueprint) 



login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)



from .models import User

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

with app.app_context():
    user = User()
    db.create_all()
