from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from settings import (
    MAX_CUSTOM_SHORT_LENGTH, MAX_ORIGINAL_LENGTH, REGEXP_FOR_SHORT
)


ORIGINAL_LABEL = 'Длинная ссылка'
SHORT_LABEL = 'Ваш вариант короткой ссылки'
SUBMIT_LABEL = 'Создать'
REQUIRED_FIELD_MESSAGE = 'Обязательное поле'
REGEXP_VALIDATION_MESSAGE = 'Допустимы латинские буквы и цифры'


class YaCutForm(FlaskForm):
    original_link = URLField(
        ORIGINAL_LABEL,
        validators=[
            Length(max=MAX_ORIGINAL_LENGTH),
            DataRequired(message=REQUIRED_FIELD_MESSAGE)
        ]
    )
    custom_id = StringField(
        SHORT_LABEL,
        validators=[
            Length(max=MAX_CUSTOM_SHORT_LENGTH),
            Regexp(
                REGEXP_FOR_SHORT,
                message=REGEXP_VALIDATION_MESSAGE
            ),
            Optional()
        ]
    )
    submit = SubmitField(SUBMIT_LABEL)
