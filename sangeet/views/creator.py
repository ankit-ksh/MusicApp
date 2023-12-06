# Implementing creator pages

from flask import (
    Blueprint, redirect, render_template, request, session, url_for
)
from sangeet.extensions import db
from flask_login import (
    login_user,
    logout_user,
    login_required,
)

bp = Blueprint('creator', __name__)


@bp.route('/creator/dashboard')
def dashboard():
    return render_template('creator/dashboard.html')

