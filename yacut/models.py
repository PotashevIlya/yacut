from datetime import datetime

from flask import url_for

from . import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String, nullable=False)
    short = db.Column(db.String, nullable=False, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self, short_link=False):
        if short_link:
            return dict(
                url=self.original,
                short_link=url_for(
                    'redirect_view',
                    short_link=self.short,
                    _external=True
                )
            )
        return dict(url=self.original)

    def from_dict(self, data):
        setattr(self, 'original', data['url'])
        setattr(self, 'short', data['custom_id'])
