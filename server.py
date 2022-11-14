from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
# create Flask instance
app = Flask(__name__)
CORS(app)
# should load this from env
app.config['SECRET_KEY'] = 'super-secret'

jwt = JWTManager(app)

@app.route("/")

# Members API Route
@app.route("/members")
def members():
    return {"members": ["Member1", "Member2", "Member3"]}

if __name__ == "__main__":
    app.run(debug=True, port=5000)