from flask import current_app
from flask_wtf import Form
from wtforms.fields import SubmitField, TextAreaField, HiddenField

class CommentForm(Form):
    lift_id = HiddenField('Lift Id')
    text = TextAreaField('Comment')
    submit = SubmitField('Submit')
