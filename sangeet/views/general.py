# Implementing user pages

from flask import (
    Blueprint, redirect, render_template, request, session, url_for, flash
)
from sangeet.extensions import db
from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)
from sangeet.models import *
from sangeet.utils.general import *

bp = Blueprint('general', __name__)


@bp.route('/home')
@login_required
def home():
    categories = [
        {'title': 'All songs', 'cat_link':'all', 'table': Track},
        {'title': 'Recently on Sangeet', 'cat_link':'recents', 'table': Track, 'order_by':'release_date'},
        ]
    content = content_overview(categories)
    # Return the result
    return render_template('general/home.html', content=content)

@bp.route('/explore')
def explore():
    categories = [
        {'title': 'All songs', 'cat_link':'all', 'table': Track, 'order_by': 'release_date'},
        {'title': 'Top Pop', 'cat_link':'pop', 'table': Track, 'filter_by': 'genre', 'value': 'pop'},
        {'title': 'Romantic Tunes', 'cat_link':'romantic', 'table': Track, 'filter_by': 'genre', 'value': 'Romantic'},
        {'title': 'English', 'cat_link':'english', 'table': Track, 'filter_by': 'name', 'value': 'English', 'table_2':Language},
        {'title': 'Devotional', 'cat_link':'devotional', 'table': Track, 'filter_by': 'genre', 'value': 'devotional'},
        {'title': 'From the Nightingale of India', 'cat_link':'lata', 'table': Track, 'filter_by': 'artist_name', 'value': 'Lata Mangeshkar'}
        ]
    content = content_overview(categories)
    # Return the result
    return render_template('general/explore.html', content=content)

    

# @bp.route('/playlist/<data>')     # to get any data about a playlist
# def get_playlist_data(data):
#     if request.method == 'POST':
#         playlist_id = request.form.get('playlist_id')
#         playlist = db.session.get(Playlist, playlist_id)
#         if data == 'tracks':
#             query_result = playlist.tracks
#             tracks = [entry for entry in query_result]
#             return tracks
#     return redirect(request.referrer)

@bp.route('/album/<data>')
def get_album_data(data):
    if request.method == 'POST':
        album_id = request.form.get('album_id')
        album = db.session.get(Album, album_id)








@bp.route('/library')
def library():
    return render_template('general/library.html')

@bp.route('/my_playlists')
def my_playlist():
    return render_template('music/playlist_listings.html')

@bp.route('/profile')
def profile():
    return render_template('general/profile.html')

@bp.route('/preferences')
def preferences():
    return render_template('general/preferences.html')

@bp.route('/test/<int:test_id>', methods=['GET', 'POST'])
def test(test_id):
    # return render_template('general/test.html', english_songs=english_songs)
    # return render_template('admin/track_listing.html', english_songs=english_songs)

    return render_template(f'test/test_{test_id}.html')