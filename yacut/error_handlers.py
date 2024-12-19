from flask import jsonify, render_template

from . import app, db
from settings import PAGE_NOT_FOUND_STATUS_CODE, INTERNAL_ERROR_STATUS_CODE


class InvalidAPIUsage(Exception):

    def __init__(self, message, status_code):
        super().__init__()
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        return dict(message=self.message)


class ShortGeneratingError(Exception):

    def __init__(self, message, status_code):
        super().__init__()
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        return dict(message=self.message)


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(ShortGeneratingError)
def short_generating_error(error):
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), PAGE_NOT_FOUND_STATUS_CODE


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), INTERNAL_ERROR_STATUS_CODE
