from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from settings import PAGE_NOT_FOUND_STATUS_CODE, BAD_REQUEST_STATUS_CODE, OK_STATUS_CODE, CREATED_STATUS_CODE


SHORT_NOT_FOUND_MESSAGE = 'Указанный id не найден'
EMPTY_REQUEST_BODY_MESSAGE = 'Отсутствует тело запроса'
NO_URL_IN_BODY_MESSAGE = '"url" является обязательным полем!'


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_original_link(short):
    urlmap = URLMap.get_url_map_object(short)
    if urlmap is None:
        raise InvalidAPIUsage(
            SHORT_NOT_FOUND_MESSAGE,
            PAGE_NOT_FOUND_STATUS_CODE
        )
    return jsonify({'url': urlmap.original}), OK_STATUS_CODE


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    data = request.get_json(silent=True)
    if data is None:
        raise InvalidAPIUsage(
            EMPTY_REQUEST_BODY_MESSAGE,
            BAD_REQUEST_STATUS_CODE
        )
    if 'url' not in data:
        raise InvalidAPIUsage(
            NO_URL_IN_BODY_MESSAGE,
            BAD_REQUEST_STATUS_CODE
        )
    url_map = URLMap.create_url_map_object(
        data.get('url'),
        data.get('custom_id')
    )
    return jsonify(url_map.to_dict()), CREATED_STATUS_CODE
