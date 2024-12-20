from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import (
    InvalidAPIUsage, ObjectCreationError
)
from .models import URLMap


SHORT_NOT_FOUND_MESSAGE = 'Указанный id не найден'
EMPTY_REQUEST_BODY_MESSAGE = 'Отсутствует тело запроса'
NO_URL_IN_BODY_MESSAGE = '"url" является обязательным полем!'


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_original_link(short):
    url_map = URLMap.get(short)
    if url_map is None:
        raise InvalidAPIUsage(
            SHORT_NOT_FOUND_MESSAGE,
            HTTPStatus.NOT_FOUND
        )
    return jsonify({'url': url_map.original}), HTTPStatus.OK


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
            data.get('custom_id'),
            validation=True
        )
    except ObjectCreationError as e:
        raise InvalidAPIUsage(str(e), status_code=HTTPStatus.BAD_REQUEST)
    return jsonify(url_map.to_dict()), HTTPStatus.CREATED
