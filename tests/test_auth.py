from flask import url_for
import json

def test_jwt_authentication_failure(client):
    url = url_for('_default_auth_request_handler')
    data = {
        'email': 'not_a_user@example.com',
        'password': 'password'
    }
    response = client.post(url, data=json.dumps(data), content_type='application/json')
    assert response.status_code == 401

def test_jwt_authentication_success(client, user):
    url = url_for('_default_auth_request_handler')
    data = {
        'email': user.email,
        'password': user.password
    }
    response = client.post(url, data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    assert response.json['access_token'] is not None
    assert response.json['user_id'] == user.id


