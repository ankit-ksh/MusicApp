from flask import (
    Blueprint, redirect, render_template, request, session, url_for, flash, send_from_directory, current_app
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

def query_a_table(info_dict):   # function for showing any content overview and redirecting to a page with all entries by just taking a categories dictionary
    content = {}
    content['title'] = info_dict['title']
    table = info_dict['table']
    filter_by = info_dict.get('filter_by', None)
    value = info_dict.get('value', None)
    if (filter_by == 'all'):                 # If its the case of returning all items from a table
        query_result = db.session.execute(db.select(table)).scalars()
    else:           # both of the above and below queries are achiveing case insensitive matching, but in a different way
        query_result = db.session.execute(db.select(Track).where(db.func.lower(getattr(table, filter_by)).ilike(f"{value.lower()}"))).scalars()
    query_result = [result for result in query_result]
    content['items'] = query_result
    return content

# Query Tracks table for different genres
@bp.route('/genre/<category>')
def genre_based_tracks(category):
    info_dict = {'title' : f"All {category.capitalize()} Songs", 'table': Track, 'filter_by': 'genre', 'value':category}    
    if category == 'all':
        info_dict['filter_by'] = 'all'
    content = query_a_table(info_dict)
    return render_template('general/list_all_songs.html', title=info_dict['title'], tracks=content['items'])

# query for different languages
@bp.route('/language/<language_name>')
def language_tracks(language_name):
    title = f"All {language_name} songs"
    language = db.session.execute(db.select(Language).where(Language.name == language_name)).scalar()
    query_result = language.tracks
    tracks = [result for result in query_result]
    return render_template('general/list_all_songs.html', title=title, tracks=tracks)

# query for different languages
@bp.route('/album/<int:album_id>')
def album_tracks(album_id):
    album = db.session.execute(db.select(Album).where(Album.id == album_id)).scalar()
    query_result = album.tracks
    title = f"All songs in Album - {album.name}"
    tracks = [result for result in query_result]
    return render_template('general/list_all_songs.html', title=title, tracks=tracks)


@bp.route('/play/<filename>')
def play_song(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
