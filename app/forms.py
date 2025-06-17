from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, URL, Length
from app.config import config


class BookmarkForm(FlaskForm):
    title = StringField('Title', validators=[
        DataRequired(message="Title is required"),
        Length(min=1, max=config.MAX_TITLE_LENGTH, 
               message=f"Title must be between 1 and {config.MAX_TITLE_LENGTH} characters")
    ])
    url = StringField('URL', validators=[
        DataRequired(message="URL is required"),
        URL(message="Please enter a valid URL")
    ])
    description = TextAreaField('Description', validators=[
        DataRequired(message="Description is required"),
        Length(min=1, max=config.MAX_DESCRIPTION_LENGTH, 
               message=f"Description must be between 1 and {config.MAX_DESCRIPTION_LENGTH} characters")
    ])
    tags = StringField('Tags')
    submit = SubmitField('Submit')  # Default text, can be overridden

    def __init__(self, submit_text=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if submit_text:
            self.submit.label.text = submit_text


# Convenience classes for backwards compatibility and semantic clarity
class NewBookmarkForm(BookmarkForm):
    def __init__(self, *args, **kwargs):
        super().__init__(submit_text='Create', *args, **kwargs)


class EditBookmarkForm(BookmarkForm):
    def __init__(self, *args, **kwargs):
        super().__init__(submit_text='Update', *args, **kwargs)
