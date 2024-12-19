import random

from .models import URLMap

SYMBOLS_FOR_SHORT_ID = (
    'ABCDEFGHJKLMNOPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz1234567890'
)
SHORT_ID_LENGTH = 6


def get_unique_short_id():
    while True:
        short_id = ''.join(random.choices(
            SYMBOLS_FOR_SHORT_ID,
            k=SHORT_ID_LENGTH
        )
        )
        if URLMap.query.filter_by(short=short_id).first() is None:
            return short_id
