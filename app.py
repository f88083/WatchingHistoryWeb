from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Init. the Flask app
app = Flask(__name__)

# TODO: database


# Route to display the watching history
@app.route("/")
def index():
    return render_template("index.html")


# Route to add a new entry to the watching history
@app.route("/add", methods=["POST"])
def add():
    pass

if __name__ == "__main__":
    app.run(debug=True)
