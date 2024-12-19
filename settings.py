import os
import string

SYMBOLS_FOR_SHORT = f'{string.ascii_letters}{string.digits}'
REGEXP_FOR_SHORT = f'{r"^["}{SYMBOLS_FOR_SHORT}{r"]+$"}'
SHORT_LENGTH = 6
SHORT_GENERATING_ITERATIONS = 10
MAX_CUSTOM_SHORT_LENGTH = 16
MAX_ORIGINAL_LENGTH = 1024


SHORT_GENERATING_FAILURE_MESSAGE = (
    'Не удалось сгенерировать короткую ссылку. Попыток - {}. Попробуйте заново'
)
INVALID_SHORT_MESSAGE = 'Указано недопустимое имя для короткой ссылки'
INVALID_ORIGINAL_MESSAGE = (
    f'Оригинальная ссылка не должна превышать {MAX_ORIGINAL_LENGTH} символа'
)
SHORT_EXISTS_MESSAGE = (
    'Предложенный вариант короткой ссылки уже существует.'
)
REDIRECT_VIEW_NAME = 'redirect_view'


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')
