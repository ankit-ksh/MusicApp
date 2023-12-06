# Implementing user pages

from flask import (
    Blueprint, redirect, render_template, request, session, url_for
)
from flask_login import (
    login_user,
    logout_user,
    login_required,
)
from sangeet.extensions import db

bp = Blueprint('admin', __name__)

@bp.route('/admin/dashboard')
def dashboard():
    return render_template('admin/dashboard.html')
