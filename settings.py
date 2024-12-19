import os
import re
import string

SYMBOLS_FOR_SHORT = string.ascii_letters + string.digits
REGEXP_FOR_SHORT = r'^[' + re.escape(SYMBOLS_FOR_SHORT) + r']+$'
SHORT_LENGTH = 6
SHORT_GENERATING_ITERATIONS = 10
MAX_CUSTOM_SHORT_LENGTH = 16

OK_STATUS_CODE = 200
CREATED_STATUS_CODE = 201
BAD_REQUEST_STATUS_CODE = 400
PAGE_NOT_FOUND_STATUS_CODE = 404
INTERNAL_ERROR_STATUS_CODE = 500

SHORT_GENERATING_FAILURE_MESSAGE = (
    'Не удалось сгенерировать короткую ссылку'
)
INVALID_SHORT_MESSAGE = 'Указано недопустимое имя для короткой ссылки'
SHORT_EXISTS_MESSAGE = (
    'Предложенный вариант короткой ссылки уже существует.'
)
REDIRECT_VIEW_NAME = 'redirect_view'


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')
