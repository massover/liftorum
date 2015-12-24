import sys

from flask import Flask
import os
from .extensions import db, bootstrap, mail, migrate, s3
from .auth import jwt
from .api import configure_api_manager


def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ['CONFIG'])

    import logging
    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    app.logger.setLevel(logging.ERROR)

    from liftorum import main
    app.register_blueprint(main.blueprint)

    from liftorum import filters
    app.jinja_env.filters['timesince'] = filters.timesince

    from flask_security import Security, SQLAlchemyUserDatastore
    from liftorum.main.models import User, Role
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)

    db.init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    s3.init_app(app)
    jwt.init_app(app)

    configure_api_manager(app)
    return app

