from flask import Flask
import logging
import sys
import os
from .extensions import db, bootstrap, mail, migrate, s3, api_manager
from flask_restless import ProcessingException
from flask.ext.security import current_user

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

    from flask.ext.security import Security, SQLAlchemyUserDatastore
    from liftorum.main.models import User, Role
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)

    db.init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    s3.init_app(app)

    def authentication_preprocessor(*args, **kw):
        pass
        #if not current_user.is_authenticated():
        #    raise ProcessingException(description='Not authenticated!', code=401)

    def post_preprocessor(data=None, **kw):
        data['user_id'] = current_user.id

    # This was giving me problems.
    # https://github.com/jfinkels/flask-restless/issues/409
    db.app = app
    api_manager.init_app(
        app,
        flask_sqlalchemy_db=db,
        preprocessors={'POST': [authentication_preprocessor]}
    )
    from liftorum.main.models import Lift, Video, Comment
    api_manager.create_api(
        Lift,
        methods=['GET', 'POST', 'DELETE'],
        app=app,
        preprocessors={
            'POST':[post_preprocessor],
        }
    )
    api_manager.create_api(Video, methods=['GET', 'POST', 'DELETE'], app=app)
    api_manager.create_api(
        Comment,
        methods=['GET', 'POST', 'DELETE'],
        app=app,
        preprocessors={
            'POST':[post_preprocessor],
        }
    )

    return app

