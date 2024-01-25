from functools import wraps
from flask import abort, request, current_app
from flask_login import current_user, login_required

from sangeet.extensions import db
from sangeet.models import *

def playlist_curator_required(f):   # for playlists, checking if the user is actual curator
    @wraps(f)
    def wrapper(**kwargs):
        if (current_user.is_authenticated):
            pass
        else:
            return current_app.login_manager.unauthorized()
        # getting the data about playlist being tried to modify
        playlist_id = kwargs.get('playlist_id')
        playlist_id = request.form.get('playlist_id', playlist_id)
        playlist_id = request.args.get('playlist_id', playlist_id)
        playlist = db.session.get(Playlist, playlist_id)
        # checking if playlist exists, and if it does, check if he's the owner then only return success otherwise error
        if (playlist is not None) and (playlist.curator_id == current_user.id):
            return f(**kwargs)
        else:
            return abort(404)
    return wrapper

def creator_required(f):
    @wraps(f)
    def wrapper(**kwargs):
        if (current_user.is_authenticated):
            pass
        else:
            return current_app.login_manager.unauthorized()
        if (current_user.role == 'creator'):
            pass
        else:
            return "You're not a creator."
        return f(**kwargs)
    return wrapper

def admin_required(f):
    @wraps(f)
    def wrapper(**kwargs):
        if (current_user.is_authenticated):
            pass
        else:
            return current_app.login_manager.unauthorized()
        if (current_user.role == 'admin'):
            pass
        else:
            return "You're not an Admin."
        return f(**kwargs)
    return wrapper

def original_creator_required(f):   # for creators, checking if the user is actual creator
    @wraps(f)
    def wrapper(**kwargs):
        if (current_user.is_authenticated):
            pass
        else:
            return current_app.login_manager.unauthorized()
        if (current_user.role == 'creator'):
            pass
        else:
            return "You're not a creator. Abort with error"
        track_id = request.args.get('track_id')
        track_id = request.form.get('track_id', track_id)
        album_id = request.args.get('album_id')
        album_id = request.form.get('album_id', album_id)
        if track_id and (track_id != 'None'):   # Select tag sends 'None' string if the name of chooser is selected
            track = db.session.get(Track, track_id)
            if track and (track.creator_id == current_user.id):
                pass
            else:
                return 'Invalid request'
        if album_id and (album_id != 'None'):
            album = db.session.get(Album, album_id)
            if album and (album.creator_id == current_user.id):
                pass
            else:
                return 'Invalid request'
        return f(**kwargs)
    return wrapper
