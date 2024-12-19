import re

from flask import flash

from .error_handlers import InvalidAPIUsage
from .models import URLMap

INVALID_SHORT_ID_MESSAGE = 'Указано недопустимое имя для короткой ссылки'
SHORT_ID_EXISTS_MESSAGE = (
    'Предложенный вариант короткой ссылки уже существует.'
)


def validate_custom_id(custom_id, for_api=True):
    if re.match(r'^[a-zA-Z0-9]+$', custom_id) is None:
        if for_api is False:
            flash(INVALID_SHORT_ID_MESSAGE)
            return False
        raise InvalidAPIUsage(INVALID_SHORT_ID_MESSAGE, 400)
    if URLMap.query.filter_by(short=custom_id).first() is not None:
        if for_api is False:
            flash(SHORT_ID_EXISTS_MESSAGE)
            return False
        raise InvalidAPIUsage(SHORT_ID_EXISTS_MESSAGE, 400)
    if len(custom_id) >= 16:
        raise InvalidAPIUsage(INVALID_SHORT_ID_MESSAGE, 400)
