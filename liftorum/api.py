from flask_restless import APIManager

from .extensions import db
from .auth import authentication_preprocessor
from liftorum.main.models import Lift, Video, Comment, User

api_manager = APIManager()

def configure_api_manager(app):
    # This was giving me problems.
    # https://github.com/jfinkels/flask-restless/issues/409
    db.app = app
    api_manager.init_app(
        app,
        flask_sqlalchemy_db=db,
        preprocessors=dict(
            #POST=[authentication_preprocessor],
            #GET_MANY=[authentication_preprocessor],
        ),
    )
    api_manager.create_api(
        Lift,
        methods=['GET', 'POST', 'DELETE'],
        app=app,
        results_per_page=10,
        include_methods=['video.url'],
        postprocessors={
            'GET_MANY': [get_many_postprocessor_add_user_to_comments],
            'GET_SINGLE': [get_single_postprocessor_add_user_to_comments],
        },
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
    api_manager.create_api(
        User,
        methods=['GET', 'POST', 'DELETE'],
        app=app,
    )


def get_many_postprocessor_add_user_to_comments(result=None, search_params=None, **kw):
    for object in result['objects']:
        for comment in object['comments']:
            user = User.query.get(comment['user_id'])
            comment.update({
                'user': {
                    column.name: getattr(user, column.name)
                    for column in user.__table__.columns
                }
            })


def get_single_postprocessor_add_user_to_comments(result=None, search_params=None, **kw):
    for comment in result['comments']:
        user = User.query.get(comment['user_id'])
        comment.update({
            'user': {
                column.name: getattr(user, column.name)
                for column in user.__table__.columns
            }
        })

