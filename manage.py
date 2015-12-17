import datetime
import string
import os
import random

from flask import current_app as app
from flask_script import Manager
from flask_migrate import MigrateCommand
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

from liftorum import create_app
from liftorum.extensions import db, s3
from liftorum.main.models import Lift, User, Comment, Video

manager = Manager(create_app)

manager.add_command('db', MigrateCommand)


@manager.command
def create_testing_database():
    engine = create_engine("postgres://localhost:5432/testing")
    if not database_exists(engine.url):
        create_database(engine.url)


@manager.command
def create_development_database():
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
    user = app.extensions['security'].datastore.create_user(
        password='password',
        email='user@example.com',
        confirmed_at=datetime.datetime.now(),
        active=True
    )
    user.username = 'user'
    db.session.add(user)
    db.session.commit()
    video = Video(
        file_extension='mov'
    )
    db.session.add(video)
    db.session.commit()
    with open('tests/example.mov', 'rb') as fp:
        s3.upload_video(fp.read(), video.filename)
    lift = Lift(
        name='squat',
        reps='5',
        weight='225',
        video=video,
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


@manager.command
def generate_salt():
    import bcrypt
    print(bcrypt.gensalt())

if __name__ == '__main__':
    if os.environ.get('CONFIG') is None:
        os.environ['CONFIG'] = 'config.DevelopmentConfig'
        os.environ['AWS_ACCESS_KEY_ID'] = 'AKIAJVQTV3HOSBXTXOMQ'
        os.environ['AWS_SECRET_ACCESS_KEY'] = open('.AWS_SECRET_ACCESS_KEY').read().strip()

    manager.run()
