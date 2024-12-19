import random
import re
from datetime import datetime

from flask import url_for

from . import db
from .error_handlers import ObjectCreationError, ShortGeneratingError
from settings import (
    SYMBOLS_FOR_SHORT, SHORT_LENGTH, SHORT_GENERATING_ITERATIONS,
    SHORT_GENERATING_FAILURE_MESSAGE, REGEXP_FOR_SHORT, INVALID_SHORT_MESSAGE,
    SHORT_EXISTS_MESSAGE, MAX_CUSTOM_SHORT_LENGTH, MAX_ORIGINAL_LENGTH,
    REDIRECT_VIEW_NAME, INVALID_ORIGINAL_MESSAGE
)


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_ORIGINAL_LENGTH), nullable=False)
    short = db.Column(
        db.String(MAX_CUSTOM_SHORT_LENGTH),
        nullable=False,
        unique=True
    )
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(
                REDIRECT_VIEW_NAME,
                short=self.short,
                _external=True
            )
        )

    @staticmethod
    def generate_short():
        for i in range(SHORT_GENERATING_ITERATIONS):
            short = ''.join(random.choices(
                SYMBOLS_FOR_SHORT,
                k=SHORT_LENGTH
            )
            )
            if URLMap.get(short) is None:
                return short
            raise ShortGeneratingError(
                SHORT_GENERATING_FAILURE_MESSAGE.format(i),
            )

    @staticmethod
    def get(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def create(original, short):
        if not short:
            short = URLMap.generate_short()
        if len(short) > MAX_CUSTOM_SHORT_LENGTH:
            raise ObjectCreationError(
                INVALID_SHORT_MESSAGE
            )
        if len(original) > MAX_ORIGINAL_LENGTH:
            raise ObjectCreationError(
                INVALID_ORIGINAL_MESSAGE
            )
        if re.match(REGEXP_FOR_SHORT, short) is None:
            raise ObjectCreationError(
                INVALID_SHORT_MESSAGE
            )
        if URLMap.get(short) is not None:
            raise ObjectCreationError(
                SHORT_EXISTS_MESSAGE
            )
        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()
        return url_map

    def create_full_short_link(self):
        return url_for(REDIRECT_VIEW_NAME, short=self.short, _external=True)
