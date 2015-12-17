from flask import Blueprint, render_template, redirect, flash, \
    request, abort, jsonify
from flask_security import login_required, current_user
from werkzeug import secure_filename
from flask_jwt import jwt_required

from .forms import CommentForm
from .models import Lift, Video, Comment
from ..extensions import db, s3

blueprint = Blueprint('main', __name__, template_folder='templates')

@blueprint.route('/')
@login_required
def home():
    page = request.args.get('page') or '1'
    lifts = Lift.query.order_by(
        Lift.created_at.desc()
    ).paginate(int(page),5,True)
    return render_template(
        'main/home.html',
        lifts=lifts,
        comment_form=CommentForm()
    )

@blueprint.route('/lifts/create', methods=['GET', 'POST'])
@login_required
def create_lift():
    return render_template('main/create_lift.html')

@blueprint.route('/upload-video-to-s3', methods=['POST'])
def upload_video_to_s3():
    filename = secure_filename(request.files['file'].filename)
    file_extension = filename.rsplit('.', 1)[1]
    video = Video(file_extension=file_extension)
    db.session.add(video)
    db.session.commit()
    s3.upload_video(request.files['file'].read(), video.filename)
    return jsonify({'video_id': video.id})

@blueprint.route('/upload-video-to-s3-2', methods=['POST'])
@jwt_required()
def upload_video_to_s3_2():
    s3.upload_video(request.files['file'].read(), request.form['filename'])
    return jsonify({})

@blueprint.route('/lifts/<int:id>/delete')
@login_required
def delete_lift(id):
    lift = Lift.query.get(id)
    if not lift:
        abort(404)
    if lift.user.id != current_user.id:
        abort(401)
    if lift.video:
        s3.delete_video(lift.video.filename)
    db.session.delete(lift)
    db.session.commit()
    flash('Lift deleted successfully', 'success')
    return redirect(request.referrer)

@blueprint.route('/comments/<int:id>/delete')
@login_required
def delete_comment(id):
    comment = Comment.query.get(id)
    if not comment:
        abort(404)
    if comment.user.id != current_user.id:
        abort(401)
    db.session.delete(comment)
    db.session.commit()
    flash('Comment deleted successfully', 'success')
    return redirect(request.referrer)




