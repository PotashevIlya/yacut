from flask import abort, redirect, render_template, url_for

from . import app
from .error_handlers import ShortGeneratingError
from .forms import YaCutForm
from .models import URLMap
from settings import (
    PAGE_NOT_FOUND_STATUS_CODE, INTERNAL_ERROR_STATUS_CODE, REDIRECT_VIEW_NAME
)


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = YaCutForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        url_map = URLMap.create_url_map_object(
            form.original_link.data,
            form.custom_id.data,
            from_api=False
        )
    except ShortGeneratingError:
        abort(INTERNAL_ERROR_STATUS_CODE)
    if not url_map:
        return render_template('index.html', form=form)
    return render_template(
        'index.html',
        form=form,
        link=url_for(REDIRECT_VIEW_NAME, short=url_map.short, _external=True)
    )


@app.route('/<string:short>')
def redirect_view(short):
    url_map = URLMap.get_url_map_object(short)
    if url_map is None:
        abort(PAGE_NOT_FOUND_STATUS_CODE)
    return redirect(url_map.original)
