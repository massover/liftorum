import datetime
import os
from urllib.parse import urljoin
from flask import url_for
from flask import current_app
from flask_user import UserMixin

from ..extensions import db

class Lift(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    name = db.Column(db.Enum('squat', 'bench', 'deadlift', name='lift_names'), nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))
    comments = db.relationship(
        'Comment',
        cascade='all,delete-orphan',
        backref='lift',
    )

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    extension = db.Column(db.String(8), nullable=False)
    lift = db.relationship(
        'Lift',
        cascade='all, delete-orphan',
        backref='video',
        uselist=False
    )

    @property
    def src(self):
        return '%s/%s/%d.%s' % (
            current_app.config['AWS_URL'],
            current_app.config['AWS_BUCKET'],
            self.id,
            self.extension
        )

    @property
    def filename(self):
        return '%d.%s' % (self.id, self.extension)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    text = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    lift_id = db.Column(db.Integer, db.ForeignKey('lift.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, default='')
    reset_password_token = db.Column(db.String(100), nullable=False, default='')
    email = db.Column(db.String(255), nullable=False, unique=True)
    confirmed_at = db.Column(db.DateTime())
    active = db.Column('is_active', db.Boolean(), nullable=False, default=False)

    lifts = db.relationship('Lift', backref='user', cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='user', cascade='all, delete-orphan')

