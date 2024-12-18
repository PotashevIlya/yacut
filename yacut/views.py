import random

from flask import abort, flash, redirect, render_template

from . import app, db
from .forms import YaCutForm
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


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = YaCutForm()
    if form.validate_on_submit():
        original = form.original_link.data
        short = form.custom_id.data
        if not short:
            short = get_unique_short_id()
        if URLMap.query.filter_by(short=short).first() is not None:
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('main_page.html', form=form)
        urlmap = URLMap(
            original=original,
            short=short
        )
        db.session.add(urlmap)
        db.session.commit()
        return render_template('main_page.html', form=form, urlmap=urlmap)
    return render_template('main_page.html', form=form)


@app.route('/<string:short_link>')
def redirect_view(short_link):
    urlmap = URLMap.query.filter_by(short=short_link).first()
    if urlmap is None:
        abort(404)
    return redirect(urlmap.original)

