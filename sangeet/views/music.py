from flask import (
    Blueprint, redirect, render_template, request, session, url_for, flash
)
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import (
    login_user,
    logout_user,
    login_required,
)
from sangeet.views import user, creator, admin
from sangeet.models import *


bp = Blueprint('music', __name__, url_prefix='/music')

@bp.route('/all')
def all_tracks():
    query_result = db.session.execute(db.select(Track)).scalars()
    song_list = [result for result in query_result]

    return render_template('general/list_all_songs.html', title='All Songs', songs=song_list)

@bp.route('/english')
def english_tracks():
    return render_template('general/list_all_songs.html', list_type='english')

@bp.route('/hindi')
def hindi_tracks():
    return render_template('general/list_all_songs.html', list_type='hindi')

@bp.route('/pop')
def pop_tracks():
    query_result = db.session.execute(db.select(Track).where(Track.genre == 'pop')).scalars()
    song_list = [result for result in query_result]
    return render_template('general/list_all_songs.html', list_type='pop', title='All Pop Songs', songs=song_list)

@bp.route('/devotional')
def devotional_tracks():
    query_result = db.session.execute(db.select(Track).where(Track.genre == 'devotional')).scalars()
    song_list = [result for result in query_result]
    return render_template('general/list_all_songs.html', list_type='pop', title='All Devotional Songs', songs=song_list)

@bp.route('/romantic')
def romantic_tracks():
    query_result = db.session.execute(db.select(Track).where(Track.genre == 'romantic')).scalars()
    song_list = [result for result in query_result]
    return render_template('general/list_all_songs.html', list_type='pop', title='All Romantic Songs', songs=song_list)

@bp.route('/trending')
def trending_tracks():
    query_result = db.session.execute(db.select(Track)).scalars()
    result = [result for result in query_result]
    return render_template('general/list_all_songs.html', list_type='trending')

@bp.route('/regional')
def regional_tracks():
    query_result = db.session.execute(db.select(Track).where(Track.genre == 'regional')).scalars()
    song_list = [result for result in query_result]
    return render_template('general/list_all_songs.html', list_type='pop', title='All Regional Songs', songs=song_list)
