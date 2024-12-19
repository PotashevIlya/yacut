from flask import abort, redirect, render_template

from . import app, db
from .forms import YaCutForm
from .models import URLMap
from .utils import get_unique_short_id
from .validators import validate_custom_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = YaCutForm()
    if form.validate_on_submit():
        original = form.original_link.data
        short = form.custom_id.data
        if not short:
            short = get_unique_short_id()
        if validate_custom_id(short, for_api=False) is False:
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
