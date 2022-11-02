from flask import Flask
from flask_cors import CORS

# create Flask instance
app = Flask(__name__)
CORS(app)

@app.route("/")

# Members API Route
@app.route("/members")
def members():
    return {"members": ["Member1", "Member2", "Member3"]}

if __name__ == "__main__":
    app.run(debug=True, port=5000)