import os
import datetime

import pytest

from liftorum import create_app
from liftorum.extensions import db
from liftorum.main.models import User

@pytest.fixture
def app():
    os.environ["CONFIG"] = 'config.TestingConfig'
    app = create_app()
    db.drop_all()
    db.create_all()
    return app

@pytest.fixture
def user(app):
    user = app.extensions['security'].datastore.create_user(
        username='user',
        password='password',
        email='user@example.com',
        confirmed_at=datetime.datetime.now(),
        active=True
    )
    return user



