import click
from flask import Blueprint
from . import main
from .models import User, WatchingHistory, db

app = Blueprint('commands', __name__)

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