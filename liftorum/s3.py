from boto.s3.connection import S3Connection
from boto.s3.key import Key

class S3(object):
    def __init__(self, app=None):
        if app is not None:
            self.app = self.init_app(app)
        else:
            self.app = app


    def init_app(self, app):
        self.app = app
        self.connection = S3Connection(
            self.app.config['AWS_ACCESS_KEY_ID'],
            self.app.config['AWS_SECRET_ACCESS_KEY'],
            host='s3-us-west-2.amazonaws.com'
        )

    def upload_video(self, data, filename):
        bucket = self.connection.get_bucket(self.app.config['AWS_BUCKET'])
        key = Key(bucket)
        key.key = filename
        key.set_contents_from_string(data)
        key.set_acl('public-read')

    def delete_video(self, filename):
        bucket = self.connection.get_bucket(self.app.config['AWS_BUCKET'])
        key = Key(bucket)
        key.key = filename
        bucket.delete_key(key)

