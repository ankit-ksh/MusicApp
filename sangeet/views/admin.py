# Implementing user pages

from flask import (
    Blueprint, redirect, render_template, request, session, url_for, flash
)
from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)
from sangeet.extensions import db
from sangeet.models import *
from sangeet.utils.general import *
from sangeet.utils.decorators import *

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/dashboard')
def dashboard():
    tables = [User, Creator, Genre, Language, Album, Playlist]
    sangeet_data = {}
    for table in tables:
        sangeet_data[table.__tablename__] = dict(
            total_in_number = len([item for item in db.session.execute(db.select(table)).scalars()])
        )
    template_data = dict(
        sangeet_data=sangeet_data
    )
    return render_template('admin/dashboard.html', **template_data)

@bp.route('/<action>/<item_type>')
@admin_required
def take_action(**kwargs):
    tables = {'track':Track, 'album':Album}
    item_type = kwargs.get('item_type')
    item_id = request.args.get('item_id')
    action = kwargs.get('action')
    item = db.session.get(tables.get(item_type), item_id)
    print(item.is_flagged)
    if action == 'flag':
        item.is_flagged = True
    elif action == 'unflag':
        item.is_flagged = False
    elif action == 'delete':
        db.session.delete(item)
    try:
        db.session.commit()
        print(item.is_flagged)
    except:
        db.session.rollback()
        return 'Something went wrong'
    return redirect(request.referrer)
