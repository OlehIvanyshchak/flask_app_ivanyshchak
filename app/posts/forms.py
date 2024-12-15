from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    DateField,
    SelectField,
    StringField,
    TextAreaField,
    SubmitField,
)
from wtforms.validators import DataRequired, Length
CATEGORIES = [
    ("tech", "Technology"),
    ("science", "Science"),
    ("lifestyle", "Lifestyle"),
]


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(2)])
    content = TextAreaField(
        "Content", render_kw={"rows": 5, "cols": 40}, validators=[DataRequired()]
    )
    is_active = BooleanField("Active Post")
    publish_date = DateField(
        "Publish Date", format="%Y-%m-%d", validators=[DataRequired()]
    )
    category = SelectField("Category", choices=CATEGORIES,
                           validators=[DataRequired()])
    submit = SubmitField("Add Post")
