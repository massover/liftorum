from flask import Blueprint, request, jsonify
from flask_jwt import jwt_required

from ..extensions import s3

blueprint = Blueprint('main', __name__, template_folder='templates')


@blueprint.route('/upload-video-to-s3', methods=['POST'])
@jwt_required()
def upload_video_to_s3_2():
    s3.upload_video(request.files['file'].read(), request.form['filename'])
    return jsonify({})
