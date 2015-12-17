from boto.s3.connection import S3Connection
from boto.s3.key import Key

class S3(object):
    def __init__(self, app=None):
        self.app = app

    def init_app(self, app):
        self.app = app

    def upload_video(self, data, filename):
        connection = S3Connection(
            self.app.config['AWS_ACCESS_KEY_ID'],
            self.app.config['AWS_SECRET_ACCESS_KEY'],
            host='s3-us-west-2.amazonaws.com'
        )
        bucket = connection.get_bucket(self.app.config['AWS_BUCKET'])
        key = Key(bucket)
        key.key = filename
        key.set_contents_from_string(data)
        key.set_acl('public-read')

    def delete_video(self, filename):
        connection = S3Connection(
            self.app.config['AWS_ACCESS_KEY_ID'],
            self.app.config['AWS_SECRET_ACCESS_KEY'],
            host='s3-us-west-2.amazonaws.com'
        )
        bucket = connection.get_bucket(self.app.config['AWS_BUCKET'])
        key = Key(bucket)
        key.key = filename
        bucket.delete_key(key)

