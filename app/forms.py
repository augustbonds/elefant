from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, URL, Length


class NewBookmarkForm(FlaskForm):
    title = StringField('Title', validators=[
        DataRequired(message="Title is required"),
        Length(min=1, max=200, message="Title must be between 1 and 200 characters")
    ])
    url = StringField('URL', validators=[
        DataRequired(message="URL is required"),
        URL(message="Please enter a valid URL")
    ])
    description = TextAreaField('Description', validators=[
        DataRequired(message="Description is required"),
        Length(min=1, max=1000, message="Description must be between 1 and 1000 characters")
    ])
    tags = StringField('Tags')
    submit = SubmitField('Create')


class EditBookmarkForm(FlaskForm):
    title = StringField('Title', validators=[
        DataRequired(message="Title is required"),
        Length(min=1, max=200, message="Title must be between 1 and 200 characters")
    ])
    url = StringField('URL', validators=[
        DataRequired(message="URL is required"),
        URL(message="Please enter a valid URL")
    ])
    description = TextAreaField('Description', validators=[
        DataRequired(message="Description is required"),
        Length(min=1, max=1000, message="Description must be between 1 and 1000 characters")
    ])
    tags = StringField('Tags')
    submit = SubmitField('Update')
