from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_migrate import Migrate

from .s3 import S3

db = SQLAlchemy()
bootstrap = Bootstrap()
mail = Mail()
s3 = S3()
migrate = Migrate()
