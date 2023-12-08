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
from sangeet.models import *

bp = Blueprint('general', __name__)



@bp.route('/home')
@login_required
def home():
    return render_template('general/home.html')

@bp.route('/explore')
def explore():
    songs = {}
    # fetching overview for english tracks
    # query_result = db.session.execute(db.select(User).where(Track.language == 'english').limit(5)).scalars()
    # fetching overview for hindi tracks
    # query_result = db.session.execute(db.select(User).where(Track.language == 'hindi').limit(5)).scalars()
    # fetching overview for Pop tracks
    query_result = db.session.execute(db.select(Track).where(Track.genre == 'pop').limit(5)).scalars()
    pop = [result for result in query_result]
    songs['pop'] = pop
    # fetching overview for english tracks
    # query_result = db.session.execute(db.select(User).where(Track.language == 'english').limit(5)).scalars()
    return render_template('general/explore.html', tracks=songs)

@bp.route('/library')
def library():
    return render_template('general/library.html')

@bp.route('/profile')
def profile():
    return render_template('general/profile.html')

@bp.route('/preferences')
def preferences():
    return render_template('general/preferences.html')

