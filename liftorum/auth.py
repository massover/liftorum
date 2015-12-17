from flask import current_app, jsonify
from flask_jwt import JWT, jwt_required
from flask_security.utils import verify_password
from werkzeug.local import LocalProxy

user_datastore = LocalProxy(lambda: current_app.extensions['security'].datastore)

jwt = JWT()

@jwt.authentication_handler
def authentication_handler(email, password):
    user = user_datastore.find_user(email=email.lower())
    if user and verify_password(password, user.password):
        return user
    return None


@jwt.identity_handler
def identity_handler(payload):
    user = user_datastore.find_user(id=payload['identity'])
    return user


@jwt.auth_response_handler
def auth_response_handler(access_token, identity):
    return jsonify({
        'access_token': access_token.decode('utf-8'),
        'user_id': identity.id
    })


@jwt_required()
def authentication_preprocessor(**kw):
    pass