# Implementing playlist pages

from flask import (
    Blueprint, redirect, render_template, request, session, url_for, current_app, flash, abort
)
import os
from werkzeug.utils import secure_filename
from sangeet.extensions import db
from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)
from sangeet.models import *
from sangeet.utils.general import *
from sangeet.utils.decorators import *

bp = Blueprint('playlist', __name__, static_folder='static', url_prefix='/playlist')

# create playlist | C in CRUD
@bp.route("/create", methods=['POST', 'GET'])
@login_required
def create_playlist():
    if request.method == 'POST':
        playlist_name = request.form.get('playlist_name')
        new_playlist = Playlist(name=playlist_name, curator_id=current_user.id)
        # adding all the track_id into a list
        tracks_to_add = [] # a list of track_id
        form_dict = request.form.to_dict()
        for key in form_dict:
            if key[0:5] == 'track':
                tracks_to_add.append(int(form_dict[key]))
        if tracks_to_add:
            for track_id in tracks_to_add:
                track_to_add = db.session.get(Track, track_id)
                new_playlist.tracks.append(track_to_add)
        db.session.add(new_playlist)
        try:
            db.session.commit()
        except Exception as e:
            return e
        return redirect(f"/playlist/{new_playlist.id}")
    return render_template('general/create_playlist.html', track_list=get_top_n(Track, 20))


# page for playlists | R in CRUD
@bp.route('/<int:playlist_id>')
@playlist_curator_required
def playlist_page(**kwargs):
    playlist_id = kwargs.get('playlist_id')
    playlist = db.session.get(Playlist, playlist_id)
    playlist_tracks = playlist.tracks
    tracks = [result for result in playlist_tracks]
    tracks = refine_track_data(tracks, page_type='playlist', playlist=playlist)
    template_data = dict(
        tracks=tracks,
        content=playlist,
        main_category='playlist',
        # music_access=music_access
    )
    return render_template('music/playlist/playlist_overview_page.html', **template_data)

# to modify any playlist's data | U & D in CRUD
@bp.route('/modify/<action>', methods=['GET', 'POST'])
@playlist_curator_required
def modify_playlist(action):
    playlist_id = request.form.get('playlist_id')
    playlist_id = request.args.get('playlist_id', playlist_id)
    playlist = db.session.get(Playlist, playlist_id)
    if playlist and (action == 'append_track'):
        track_id = request.form.get('track_id')
        track = db.session.get(Track, track_id)
        if track in playlist.tracks:
            flash('Track is already part of that playlist', 'error')
            return redirect(request.referrer)
        playlist.tracks.append(track)
    elif playlist and (action == 'remove_track'):
        track_id = request.form.get('track_id')
        track = db.session.get(Track, track_id)
        playlist.tracks.remove(track)
        db.session.commit()
    elif playlist and (action == 'rename'):
        new_name = request.form.get('new_name')
        playlist.name = new_name
    elif playlist and (action == 'delete'):
        db.session.delete(playlist)
        db.session.commit()
        return redirect(url_for('general.library'))
    else:
        return redirect(request.referrer)
    try:
        db.session.commit()
    except:
        abort(501)
    return redirect(request.referrer)

@bp.route('/test/<string>')
def test(**kwargs):
    return kwargs