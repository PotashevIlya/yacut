from http import HTTPStatus
from flask import jsonify, request, render_template

from . import app
from .error_handlers import (
    InvalidAPIUsage, ShortGeneratingError, ObjectCreationError
)
from .models import URLMap


SHORT_NOT_FOUND_MESSAGE = 'Указанный id не найден'
EMPTY_REQUEST_BODY_MESSAGE = 'Отсутствует тело запроса'
NO_URL_IN_BODY_MESSAGE = '"url" является обязательным полем!'


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_original_link(short):
    urlmap = URLMap.get(short)
    if urlmap is None:
        raise InvalidAPIUsage(
            SHORT_NOT_FOUND_MESSAGE,
            HTTPStatus.NOT_FOUND
        )
    return jsonify({'url': urlmap.original}), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    data = request.get_json(silent=True)
    if data is None:
        raise InvalidAPIUsage(
            EMPTY_REQUEST_BODY_MESSAGE,
        )
    if 'url' not in data:
        raise InvalidAPIUsage(
            NO_URL_IN_BODY_MESSAGE,
        )
    try:
        url_map = URLMap.create(
            data['url'],
            data.get('custom_id')
        )
    except ShortGeneratingError as e:
        raise InvalidAPIUsage(
            str(e),
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR
        )
    except ObjectCreationError as e:
        raise InvalidAPIUsage(str(e))
    return jsonify(url_map.to_dict()), HTTPStatus.CREATED


@app.route('/redoc')
def get_api_specification():
    return render_template('redoc.html')
