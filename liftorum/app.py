from flask import Flask, jsonify
import logging
import sys
import os
from .extensions import db, bootstrap, mail, migrate, s3, api_manager, jwt
from flask_restless import ProcessingException
from flask.ext.security import current_user
from flask.ext.security.utils import verify_password
from flask_jwt import current_identity

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

    @jwt.authentication_handler
    def authenticate(email, password):
        user = user_datastore.find_user(email=email)
        if user and verify_password(password, user.password):
            return user
        return None

    @jwt.identity_handler
    def identity(payload):
        user = user_datastore.find_user(id=payload['identity'])
        return user

    @jwt.auth_response_handler
    def auth_response(access_token, identity):
        return jsonify({
            'access_token': access_token.decode('utf-8'),
            'user_id': identity.id
        })

    jwt.init_app(app)

    def authentication_preprocessor(*args, **kw):
        pass
        #if not current_user.is_authenticated():
        #    raise ProcessingException(description='Not authenticated!', code=401)

    def post_preprocessor(data=None, **kw):
        #data['user_id'] = current_user.id
        pass

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

