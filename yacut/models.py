import random
import re
from datetime import datetime

from flask import flash, url_for

from . import db
from .error_handlers import InvalidAPIUsage, ShortGeneratingError
from settings import (
    SYMBOLS_FOR_SHORT, SHORT_LENGTH, SHORT_GENERATING_ITERATIONS,
    SHORT_GENERATING_FAILURE_MESSAGE, REGEXP_FOR_SHORT, INVALID_SHORT_MESSAGE,
    SHORT_EXISTS_MESSAGE, BAD_REQUEST_STATUS_CODE, MAX_CUSTOM_SHORT_LENGTH,
    REDIRECT_VIEW_NAME, INTERNAL_ERROR_STATUS_CODE
)


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String, nullable=False)
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
    def get_url_map_object(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def create_url_map_object(original, short, from_api=True):
        if not short:
            for _ in range(SHORT_GENERATING_ITERATIONS):
                short = ''.join(random.choices(
                    SYMBOLS_FOR_SHORT,
                    k=SHORT_LENGTH
                )
                )
                if URLMap.get_url_map_object(short) is None:
                    short = short
                    break
                raise ShortGeneratingError(
                    SHORT_GENERATING_FAILURE_MESSAGE,
                    INTERNAL_ERROR_STATUS_CODE
                )
        if re.match(REGEXP_FOR_SHORT, short) is None:
            if not from_api:
                flash(INVALID_SHORT_MESSAGE)
                return False
            raise InvalidAPIUsage(
                INVALID_SHORT_MESSAGE,
                BAD_REQUEST_STATUS_CODE
            )
        if URLMap.get_url_map_object(short) is not None:
            if not from_api:
                flash(SHORT_EXISTS_MESSAGE)
                return False
            raise InvalidAPIUsage(
                SHORT_EXISTS_MESSAGE,
                BAD_REQUEST_STATUS_CODE
            )
        if len(short) > MAX_CUSTOM_SHORT_LENGTH:
            raise InvalidAPIUsage(
                INVALID_SHORT_MESSAGE,
                BAD_REQUEST_STATUS_CODE
            )
        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()
        return url_map
