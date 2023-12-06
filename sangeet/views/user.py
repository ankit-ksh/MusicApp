# Implementing user pages

from flask import (
    Blueprint, redirect, render_template, request, session, url_for
)
from sangeet.extensions import db
from flask_login import (
    login_user,
    logout_user,
    login_required,
)


bp = Blueprint('user', __name__)


@bp.route('/register_as_creator')
def register_as_creator():
    return render_template('general/register_as_creator.html')