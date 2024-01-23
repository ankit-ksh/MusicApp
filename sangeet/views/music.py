from flask import (
    Blueprint, redirect, render_template, request, session, url_for, flash, send_from_directory, current_app
)
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)
from sangeet.views import user, creator, admin
from sangeet.models import *
from sangeet.utils.general import *


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

# # Query Tracks table for different genres
# @bp.route('/genre/<category>')
# def genre_based_tracks(category):
#     info_dict = {'title' : f"All {category.capitalize()} Songs", 'table': Track, 'filter_by': 'genre', 'value':category}    
#     if category == 'all':
#         info_dict['filter_by'] = 'all'
#     content = query_a_table(info_dict)
#     return render_template('general/list_all_songs.html', title=info_dict['title'], tracks=content['items'])

# # query for different languages
# @bp.route('/language/<language_name>')
# def language_tracks(language_name):
#     title = f"All {language_name} songs"
#     language = db.session.execute(db.select(Language).where(Language.name == language_name)).scalar()
#     query_result = language.tracks
#     tracks = [result for result in query_result]
#     return render_template('music/music_overview_page.html', content=language, tracks=tracks)

# # page for albums
# @bp.route('/album/<int:album_id>')
# def album_page(album_id):
#     try:
#         album = db.session.get(Album, album_id)
#         album_tracks = album.tracks
#     except:
#         return 'Something went wrong'
#     tracks = [result for result in album_tracks]
#     return render_template('music/music_overview_page.html', tracks=tracks, content=album, context_specific_track_options='layouts/empty_page.html')




@bp.route('/all/<content_type>')
@login_required
def all_content(content_type):
    if content_type == 'tracks':
        query_result = db.session.execute(db.select(Track)).scalars()
        tracks = [entry for entry in query_result]
        tracks = refine_track_data(tracks)
        return render_template('music/all_music_page.html', tracks=tracks, title="All tracks on Sangeet")

# show all of a category
@bp.route('/<category>/<category_id>')
@login_required
def overview_of_category(category, category_id):
    category_dict = dict(
        playlist = Playlist,
        language = Language,
        album = Album,
        genre = Genre,
        creator = Creator,
    )
    if category in category_dict:
        content = db.session.get(category_dict.get(category), category_id)
        tracks = content.tracks[:10]
        return render_template(
            'music/music_overview_page.html', **dict(
            tracks=refine_track_data(tracks),
            main_category = category,
            content = content
            ))


# show all of a category
@bp.route('/all/<category>/<category_id>')
@login_required
def all_content_of_category(category, category_id):
    category_dict = dict(
        playlist = Playlist,
        language = Language,
        album = Album,
        genre = Genre,
        creator = Creator,
    )
    if category in category_dict:
        category_object = db.session.get(category_dict.get(category), category_id)
        tracks = category_object.tracks
        tracks = refine_track_data(tracks)
        return render_template(
            'music/all_music_page.html', **dict(
            tracks=tracks,
            title = f"All tracks : {category_object.name.capitalize()}"
            ))

@bp.route('/play/<filename>')
def play_song(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
