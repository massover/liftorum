import os
import logging
import sys

_this_directory = os.path.dirname(os.path.abspath(__file__))

class Config(object):
    BASE_DIRECTORY = _this_directory

    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', '')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', '')
    AWS_URL = 'https://s3-us-west-2.amazonaws.com'

    # Flask Security
    SECURITY_CONFIRMABLE = True
    SECURITY_REGISTERABLE = True
    SECURITY_EMAIL_SENDER = 'noreply@liftorum.com'
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT')

    # Flask Mail
    MAIL_USERNAME = os.getenv('MAILGUN_SMTP_LOGIN')
    MAIL_PASSWORD = os.getenv('MAILGUN_SMTP_PASSWORD')
    MAIL_SERVER = os.getenv('MAILGUN_SMTP_SERVER')
    MAIL_PORT = os.getenv('MAILGUN_SMTP_PORT')
    MAIL_DEFAULT_SENDER = 'Liftorum <noreply@liftorum.com>'

    ALLOWED_EXTENSIONS = set(['MOV', 'mp4'])

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    AWS_BUCKET = 'lift-videos-bucket-testing'
    SECRET_KEY = 'U6IOODCSLXIM6GJVYPXEN3VT'
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost:5432/testing'

    WTF_CSRF_ENABLED = False

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
    AWS_BUCKET = 'lift-videos-bucket-development'
    SECRET_KEY = 'U6IOODCSLXIM6GJVYPXEN3VT'
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost:5432/development'
    BUNDLE_JS = 'http://localhost:8080/bundle.js'
    STYLES_CSS = 'http://localhost:8080/styles.css'


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    AWS_BUCKET = 'lift-videos-bucket-production'
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', '')
    BUNDLE_JS = os.path.join(_this_directory, '/static/bundle.js')
    STYLES_CSS = os.path.join(_this_directory, '/static/styles.css')

