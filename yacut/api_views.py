import re

from flask import jsonify, request, url_for

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id

@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_id(short_id):
    object = URLMap.query.filter_by(short=short_id).first()
    if object is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify(object.to_dict()), 200

@app.route('/api/id/', methods=['POST'])
def create_short_link():
    data = request.get_json(silent=True)
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса', 400)
    if 'custom_id' not in data or len(data['custom_id']) == 0:
        data['custom_id'] = get_unique_short_id()
    if re.match(r'^[a-zA-Z0-9]+$', data['custom_id']) is None:
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки', 400)
    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!', 400)
    if URLMap.query.filter_by(short=data['custom_id']).first() is not None:
        raise InvalidAPIUsage('Предложенный вариант короткой ссылки уже существует.', 400)
    if len(data['custom_id']) >= 16:
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки', 400)
    urlmap = URLMap()
    urlmap.from_dict(data)
    db.session.add(urlmap)
    db.session.commit()
    return jsonify({'url': data['url'], 'short_link': url_for('redirect_view', short_link=urlmap.short, _external=True)}), 201
