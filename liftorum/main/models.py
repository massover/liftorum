import datetime

from flask import current_app
from flask.ext.security import UserMixin, RoleMixin
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
    file_extension = db.Column(db.String(8), nullable=False)
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
            self.file_extension
        )


    @property
    def url(self):
        return '%s/%s/%d.%s' % (
            current_app.config['AWS_URL'],
            current_app.config['AWS_BUCKET'],
            self.id,
            self.file_extension
        )
    @property
    def filename(self):
        return '%d.%s' % (self.id, self.file_extension)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    text = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    lift_id = db.Column(db.Integer, db.ForeignKey('lift.id'))

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    lifts = db.relationship('Lift', backref='user', cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='user', cascade='all, delete-orphan')


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
