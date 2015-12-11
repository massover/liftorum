from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask_bootstrap import Bootstrap
bootstrap = Bootstrap()

from flask_mail import Mail
mail = Mail()

from .s3 import S3
s3 = S3()

from flask_migrate import Migrate
migrate = Migrate()

from flask_restless import APIManager
api_manager = APIManager()

from flask_jwt import JWT
jwt = JWT()
