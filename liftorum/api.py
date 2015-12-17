from flask_restless import APIManager

from .extensions import db
from .auth import authentication_preprocessor
from liftorum.main.models import Lift, Video, Comment

api_manager = APIManager()

def configure_api_manager(app):
    # This was giving me problems.
    # https://github.com/jfinkels/flask-restless/issues/409
    db.app = app
    api_manager.init_app(
        app,
        flask_sqlalchemy_db=db,
        preprocessors=dict(
            POST=[authentication_preprocessor],
            GET_MANY=[authentication_preprocessor],
        ),
    )
    api_manager.create_api(
        Lift,
        methods=['GET', 'POST', 'DELETE'],
        app=app,
        results_per_page=3,
        include_methods=['video.url'],
    )
    api_manager.create_api(
        Video,
        methods=['GET', 'POST', 'DELETE'],
        app=app,
        include_methods=['url'],
    )
    api_manager.create_api(
        Comment,
        methods=['GET', 'POST', 'DELETE'],
        app=app,
    )