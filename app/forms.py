from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class NewBookmarkForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    url = StringField('Url', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Create')
