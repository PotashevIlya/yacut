import random

from flask import redirect, render_template

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
        print(form.data)
        if form.data['custom_id'] == '':
            short = get_unique_short_id()
        else:
            short = form.custom_id.data
        urlmap = URLMap(
            original=original,
            short=short
        )
        db.session.add(urlmap)
        db.session.commit()
        return render_template('main_page.html', form=form, urlmap=urlmap)
    return render_template('main_page.html', form=form)


@app.route('/<string:id>/')
def redirect_view(id):
    urlmap = URLMap.query.filter_by(short=id).first()
    return redirect(urlmap.original)

