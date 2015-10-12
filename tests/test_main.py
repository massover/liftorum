import os
from flask import url_for, request, session
from flask_testing import TestCase

import manage
from liftorum.extensions import db
from liftorum.main.models import Lift, Comment

class MainTestCase(TestCase):

    def create_app(self):
        from liftorum import create_app
        os.environ['CONFIG'] = 'config.TestingConfig'
        app = create_app()
        return app

    def setUp(self):
        manage.seed_db()
        response = self.client.get(url_for('user.login'))
        self.assertEqual(response.status_code, 200)
        with self.client.session_transaction() as session:
            session['user_id'] = 1

    def test_home(self):
        response = self.client.get(url_for('main.home'))
        self.assertEqual(response.status_code, 200)

    def test_create_lift(self):
        self.assertEqual(Lift.query.count(), 1)
        self.assertEqual(Comment.query.count(), 1)
        filename = os.path.join(self.app.config['BASE_DIRECTORY'], 'tests/example.mov')
        data = {
            'name': 'squat',
            'reps': '5',
            'weight': '225',
            'text': 'this is text to test the comment field',
            'video': (open(filename, 'rb'), 'example.MOV'),
        }
        response = self.client.post(
            url_for('main.create_lift'),
            buffered=True,
            content_type='multipart/form-data',
            data=data,
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Lift.query.count(), 2, response.data)
        self.assertEqual(Comment.query.count(), 2)

    def test_delete_lift(self):
        self.assertEqual(Lift.query.count(), 1)
        self.assertEqual(Comment.query.count(), 1)
        url = url_for('main.delete_lift', id=1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Lift.query.count(), 0)
        self.assertEqual(Comment.query.count(), 0)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_create_comment(self):
        self.assertEqual(Comment.query.count(), 1)
        data = {
            'text': 'this is text to test the comment field',
            'lift_id': '1'
        }
        url = url_for('main.create_comment')
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.query.count(), 2)

    def test_delete_comment(self):
        self.assertEqual(Comment.query.count(), 1)
        url = url_for('main.delete_comment', id=1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.query.count(), 0)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

