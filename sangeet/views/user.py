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


bp = Blueprint('user', __name__, template_folder='templates', static_folder='static', url_prefix='/user')

@bp.route('/home')
@login_required
def home():
    return render_template('user/home.html')

@bp.route('/explore')
def explore():
    return render_template('user/explore.html')

@bp.route('/library')
def library():
    return render_template('user/library.html')

@bp.route('/profile')
def profile():
    return render_template('user/profile.html')

@bp.route('/preferences')
def preferences():
    return render_template('user/preferences.html')

@bp.route('/register_as_creator')
def register_as_creator():
    return render_template('user/register_as_creator.html')