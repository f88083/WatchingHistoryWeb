from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Init. the Flask app
app = Flask(__name__)

# Config. database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///watching-history.db'
# Init. database
db = SQLAlchemy(app)

# Create a model for database
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    season = db.Column(db.String(10), nullable=False)
    value = db.Column(db.Integer, nullable=False)
    episode = db.Column(db.Integer, nullable=False)
    progress = db.Column(db.String(10), nullable=False)

    # Return a string when create a new element
    def __repr__(self):
        return '<Watching History %r>' % self.id

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
