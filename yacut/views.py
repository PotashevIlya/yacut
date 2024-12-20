from http import HTTPStatus

from flask import abort, flash, redirect, render_template

from . import app
from .error_handlers import ShortGeneratingError, ObjectCreationError
from .forms import YaCutForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = YaCutForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        url_map = URLMap.create(
            form.original_link.data,
            form.custom_id.data
        )
    except Exception as e:
        flash(e)
        return render_template('index.html', form=form)
    return render_template(
        'index.html',
        form=form,
        link=url_map.get_full_short_link()
    )


@app.route('/<string:short>')
def redirect_view(short):
    url_map = URLMap.get(short)
    if url_map is None:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(url_map.original)
