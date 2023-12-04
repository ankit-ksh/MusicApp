# Implementing user pages

from flask import (
    Blueprint, redirect, render_template, request, session, url_for
)
from sangeet.extensions import db

bp = Blueprint('admin', __name__, template_folder='templates', static_folder='static', url_prefix='/admin')

@bp.route('/home')
def home():
    return render_template('admin/home.html')

@bp.route('/explore')
def explore():
    return render_template('admin/explore.html')

@bp.route('/library')
def library():
    return render_template('admin/library.html')

@bp.route('/dashboard')
def dashboard():
    return render_template('admin/dashboard.html')


@bp.route('/profile')
def profile():
    return render_template('admin/profile.html')

@bp.route('/preferences')
def preferences():
    return render_template('admin/preferences.html')

