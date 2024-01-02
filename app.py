from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
import click
from werkzeug.security import generate_password_hash, check_password_hash


# Init. the Flask app
app = Flask(__name__)

# Config. database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///watching-history.db"
# Config. secret key
app.config['SECRET_KEY'] = 'dev' # FIXME: Should change to a random string when deploy
# Init. database
db = SQLAlchemy(app)

# Instantiate login manager
login_manager = LoginManager(app)

@app.cli.command() # Register as command
@click.option('--drop', is_flag=True, help='Create after drop.')
# Configure the command for drop and create database
def initdb(drop):
    """Initialize the database."""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')

@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
# Create a command to create an admin user
def admin(username, password):
    """Create user."""
    db.create_all()
    
    user = User.query.first()

    # Update the user if exists
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)
    else:
        click.echo('Creating user...')
        user = User(username=username, name='Admin')
        user.set_password(password)
        db.session.add(user)
    
    db.session.commit()
    click.echo('Done.')



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


@login_manager.user_loader
def load_user(user_id):
    # Return user object by searching on ID or None
    return db.session.get(User, int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'] # Get username from form
        password = request.form['password'] # Get password from form

        if not username or not password:
            flash('Invalid username or password')
            return redirect(url_for('login'))
        
        user = User.query.first()

        if username == user.username and user.validate_password(password):
            login_user(user)
            flash('Login success')
            return redirect(url_for('index'))
        
        # If username or password is wrong
        flash('Invalid username or password')

        # Back to login page
        return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout')
@login_required # Protect this route
def logout():
    logout_user()
    flash('Logout success')
    return redirect(url_for('index'))


# Route to display the watching history
@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        # 檢查登入狀態
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        # 收到資料
        history_title = request.form["title"]
        history_season = request.form["season"]
        history_value = request.form["value"]
        history_episode = request.form["episode"]
        history_progress = request.form["progress"]

        # 資料轉換為WatchingHistory class
        new_history = WatchingHistory(
            title=history_title,
            season=history_season,
            value=history_value,
            episode=history_episode,
            progress=history_progress,
        )

        try:
            # 資料加入
            db.session.add(new_history)
            db.session.commit()
            return redirect("/")
        except:
            return "There was an issue adding the history"
    else:
        # 檢查登入狀態
        if not current_user.is_authenticated:
            flash('Please login to see the history')
            return redirect(url_for('login'))
        # 獲取所有資料
        history = WatchingHistory.query.order_by(WatchingHistory.date_created).all()
        # 傳資料到index.html
        return render_template("index.html", history=history)

@app.route('/delete/<int:id>')
@login_required
def delete(id):
    # 從資料庫取得該task
    history_to_delete = WatchingHistory.query.get_or_404(id)

    try:
        # 刪除該task
        db.session.delete(history_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue deleting the history'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required    
def update(id):
    # 從資料庫取得該history
    history = WatchingHistory.query.get_or_404(id)

    if request.method == 'POST':
        # 取得用戶輸入的資料
        history.title = request.form['title']
        history.season = request.form['season']
        history.value = request.form['value']
        history.episode = request.form['episode']
        history.progress = request.form['progress']
        
        try:
            # 更新資料庫
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your history'
    else:
        return render_template('update.html', history=history)

if __name__ == "__main__":
    app.run(debug=True)
