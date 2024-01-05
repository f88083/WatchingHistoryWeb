from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Create a model for database
class WatchingHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    season = db.Column(db.String(10), nullable=False)
    value = db.Column(db.Integer, nullable=False)
    episode = db.Column(db.Integer, nullable=False)
    progress = db.Column(db.String(10), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # Return a string when create a new element
    def __repr__(self):
        return "<Watching History %r>" % self.id
    
# User class
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128)) # Hashed password

    def set_password(self, password):
        # Create hashed password
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        # Validate password
        return check_password_hash(self.password_hash, password)