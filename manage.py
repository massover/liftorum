import datetime
import os
import sys
import random
import string
from flask import current_app as app
from flask_user.passwords import hash_password
from celery.bin.celery import main as celery_main

from liftorum import create_app
from liftorum.extensions import db
from liftorum.main.models import Lift, User, Comment, Video

from flask_script import Manager
manager = Manager(create_app)

from flask_migrate import MigrateCommand
manager.add_command('db', MigrateCommand)

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

@manager.command
def create_testing_postgre_database():
    engine = create_engine("postgres://localhost:5432/testing")
    if not database_exists(engine.url):
        create_database(engine.url)

@manager.command
def create_development_postgre_database():
    engine = create_engine("postgres://localhost:5432/development")
    if not database_exists(engine.url):
        create_database(engine.url)

@manager.command
def runserver():
    app.run(threaded=True)

@manager.shell
def make_shell_context():
    return dict(app=app, db=db, Lift=Lift, User=User, Comment=Comment, Video=Video)

@manager.command
def create_db():
    db.drop_all()
    db.create_all()

@manager.command
def seed_db():
    db.drop_all()
    db.create_all()
    user = User(
        username='user',
        password=app.user_manager.hash_password('password'),
        email='user@example.com',
        confirmed_at=datetime.datetime.now(),
        active=True
    )
    db.session.add(user)
    db.session.commit()
    lift = Lift(
        name='squat',
        reps='5',
        weight='225',
        user=user,
    )
    db.session.add(lift)
    db.session.commit()
    comment = Comment(
        text='This is some text for a comment',
        lift=lift,
        user=user
    )
    db.session.add(comment)
    db.session.commit()

@manager.command
def generate_secret_key():
    secret_key = ''.join(
        random.SystemRandom().choice(string.ascii_uppercase + string.digits)
        for _ in range(24)
    )
    print(secret_key)

if __name__ == '__main__':
    if os.environ.get('CONFIG') is None:
        os.environ['CONFIG'] = 'config.DevelopmentConfig'
    manager.run()
