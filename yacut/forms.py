from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from settings import MAX_CUSTOM_SHORT_LENGTH, REGEXP_FOR_SHORT

SUBMIT_LABEL = 'Создать'


class YaCutForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле')]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(max=MAX_CUSTOM_SHORT_LENGTH),
            Regexp(
                REGEXP_FOR_SHORT,
                message='Допустимы латинские буквы и цифры'
            ),
            Optional()
        ]
    )
    submit = SubmitField(SUBMIT_LABEL)
