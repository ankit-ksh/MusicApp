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

bp = Blueprint('creator', __name__, template_folder='templates', static_folder='static', url_prefix='/creator')


@bp.route('/home')
@login_required
def home():
    return render_template('creator/home.html')

@bp.route('/explore')
def explore():
    return render_template('creator/explore.html')

@bp.route('/library')
def library():
    return render_template('creator/library.html')

@bp.route('/dashboard')
def dashboard():
    return render_template('creator/dashboard.html')

@bp.route('/profile')
def profile():
    return render_template('creator/profile.html')

@bp.route('/preferences')
def preferences():
    return render_template('creator/preferences.html')
