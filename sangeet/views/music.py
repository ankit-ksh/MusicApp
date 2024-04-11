from flask import (
    Blueprint, redirect, render_template, request, session, url_for, flash, send_from_directory, current_app, abort
)
import os
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

# all playlists, albums or genres, any resource. It can even be all users for admin's info
@bp.route('/all/<content_type>')
@login_required
def all_content(content_type):
    if content_type == 'tracks':
        query_result = db.session.execute(db.select(Track)).scalars()
        tracks = [entry for entry in query_result]
        template_data = dict(
            tracks = refine_music_data(tracks=tracks)['tracks'],
            title="All tracks on Sangeet"
        )
        return render_template('music/all_music_page.html', **template_data)

# show overview of a category
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
        template_data = dict(
            tracks=refine_music_data(tracks=tracks).get('tracks'),
            music_collection=refine_music_data(music_collection=content)['music_collection'],
            main_category = category,
            )
        return render_template('music/real_music_overview_page.html', **template_data)            


# show all tracks of a category
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
        tracks = refine_music_data(tracks=tracks).get('tracks')
        print(tracks)
        template_data = dict(
            tracks=tracks,
            title = f"All tracks [{category_object.__tablename__.capitalize()}] : {category_object.name.capitalize()}"
            )
        return render_template('music/all_music_page.html', **template_data)

@bp.route('/serve/<int:track_id>')
@login_required
def server(track_id):
    track = db.session.get(Track, track_id)
    abs_music_dir = os.path.join(os.getcwd(), current_app.config['UPLOAD_FOLDER'])
    return send_from_directory(abs_music_dir, track.file_name)

@bp.route('/player/<int:track_id>')
def player(track_id):
    track = db.session.get(Track, track_id)
    track_data = extract_track_data(track)
    if track:
        lyrics=track_data['english_lyrics']
        if not lyrics:
            lyrics = 'Lyrics Not available'
        return render_template('music/player.html', track=track, lyrics=lyrics)
    else:
        message = 'Track not available'
        return render_template('music/player.html', message=message)