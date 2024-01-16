# Implementing creator pages

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

bp = Blueprint('creator', __name__, static_folder='static')


@bp.route('/track/<action>', methods=['GET', 'POST'])
def track_actions(action):
    if action == 'upload':
        if request.method == 'POST':
            track_title = request.form.get('song_title')
            artist_name = request.form.get('artist_name')
            genre_id = request.form.get('genre_id')
            creator_id = request.form.get('creator_id')

            if 'file' not in request.files:
                return redirect(request.url)

            file = request.files['file']

            if file.filename == '':
                return redirect(request.url)

            if file:
                filename = secure_filename(file.filename)
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

                # create folder if it doesn't exist
                os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
                # Save file to the file system
                file.save(filepath)

                # Save file information to the database
                new_track = Track(name=track_title, artist_name=artist_name, creator_id=creator_id, genre_id=genre_id, file_name=filename, file_path=filepath)
                db.session.add(new_track)
                db.session.commit()
                flash('Upload Successfull', 'success')
                return redirect(request.url)
            else:
                flash('Failed', 'error')
                return redirect(request.url)
        # provide genres to select from
        query_result = db.session.execute(db.select(Genre)).scalars()
        genres = [genre for genre in query_result]
        return render_template('creator/upload_song.html', genres=genres)
    if action == 'edit':
        pass
    

@bp.route('/album/<action>', methods=['GET', 'POST'])    # any action related to albums which modifies it
def album_actions(action):
    if request.method == 'POST':
        try:
            album_id = request.form.get('album_id')
            album = db.session.get(Album, album_id)
        except:
            return redirect(request.referrer)
        if album.creator_id == current_user.id:
            pass
        else:
            flash("You're not authorized to acccess this page", 'error')
            return redirect(request.referrer)
    if action == 'append_track':
        if request.method == 'POST':
            track_id = request.form.get('track_id')
            track = db.session.get(Track, track_id)
            if track in album.tracks:
                flash('Track is already part of that album', 'error')
                return redirect(request.referrer)
            album.tracks.append(track)
            db.session.commit()
            flash(f"Track '{track.name}' was added to the playlist '{album.name}'", 'success')  
    elif action == 'create':
        if request.method == 'POST':
            # provide genres to select from
            album_name = request.form.get('album_name')
            artist_name = request.form.get('album_name')
            genre_id = request.form.get('genre_id')
            creator_id = request.form.get('creator_id')
            release_date = request.form.get('release_date')
            release_date = datetime.strptime(release_date, '%Y-%m-%d')
            description = request.form.get('description')
            new_artist = Artist(name=artist_name)
            artist_id = new_artist.id
            new_album = Album(name=album_name, artist_id=artist_id, genre_id = genre_id, creator_id=creator_id, release_date=release_date, description=description)
            db.session.add(new_artist)
            db.session.add(new_album)
            db.session.commit()
        query_result = db.session.execute(db.select(Genre)).scalars()
        genres = [genre for genre in query_result]
        return render_template('creator/create_album.html', genres)
    elif action == 'delete':
        db.session.delete(album)
        db.session.commit()
    return redirect(request.referrer)

@bp.route('/my_content/songs')
def my_songs():
    query_result = db.session.execute(db.select(Track).where(Track.creator_id == current_user.id)).scalars()
    tracks = [entry for entry in query_result]
    return render_template('creator/my_songs.html', tracks=tracks)

@bp.route('/my_content/albums')
def my_albums():
    query_result = db.session.execute(db.select(Album).where(Album.creator_id == current_user.id)).scalars()
    albums = [entry for entry in query_result]
    return render_template('creator/my_albums.html', albums=albums)

@bp.route('/delete/track', methods=['GET', 'POST'])
def delete_track():
    if request.method == 'POST':
        track_id = request.form.get('track_id')
        if not track_id:
            flash("Invalid Request", 'error')
            return redirect(request.base_url)
        track_to_delete = db.session.get(Track, track_id)
        if track_to_delete and track_to_delete.creator_id == current_user.id:
            try:
                track_name = track_to_delete.name
                db.session.delete(track_to_delete)
                db.session.commit()
                flash(f"Track Deleted : {track_name}", 'success')
                # return redirect(request.base_url)
            except Exception as e:
                db.session.rollback()
                flash(f"Error deleting track: {str(e)}", 'error')
                # return redirect(request.base_url)
        else:
            flash("Not authenticated")
            # return redirect(request.base_url)
    return redirect(request.referrer)

@bp.route('/edit/track/<track_id>', methods=['GET', 'POST'])
def edit_track(track_id):
    existing_track = db.session.get(Track, track_id)
    if request.method == 'POST':
        track_title = request.form.get('song_title')
        artist_name = request.form.get('artist_name')
        genre_id = request.form.get('genre_id')
        creator_id = request.form.get('creator_id')

        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file:
            file_name = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file_name)

            # create folder if it doesn't exist
            os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
            # Save file to the file system
            file.save(file_path)

            # update information in the database
            existing_track.name = request.form.get('song_title')
            existing_track.artist_name = request.form.get('artist_name')
            existing_track.genre_id = request.form.get('genre_id')
            existing_track.creator_id = request.form.get('creator_id')
            existing_track.file_name = request.form.get('file_name')
            existing_track.file_path = request.form.get('file_path')            
            db.session.commit()
            flash('Update Successfull', 'success')
            return redirect(request.referrer)
        else:
            flash('Failed', 'error')
            return redirect(request.url)
        
    # provide genres to select from
    genres = db.session.execute(db.select(Genre)).scalars()
    genres = [genre for genre in genres]

    # return render_template('creator/edit_track.html', genres=genres, existing_track=existing_track)
    return track_id

































# @bp.route('/delete/album', methods=['GET', 'POST'])
# def delete_album():
#     if request.method == 'POST':
#         album_id = request.form.get('album_id')
#         if not album_id:
#             flash("Invalid Request", 'error')
#             return redirect(request.base_url)
#         album_to_delete = db.session.get(Album, album_id)
#         if album_to_delete and album_to_delete.creator_id == current_user.id:
#             try:
#                 album_name = album_to_delete.name
#                 db.session.delete(album_to_delete)
#                 db.session.commit()
#                 flash(f"album Deleted : {album_name}", 'success')
#                 return redirect(request.base_url)
#             except Exception as e:
#                 db.session.rollback()
#                 flash(f"Error deleting album: {str(e)}", 'error')
#                 return redirect(request.base_url)
#         else:
#             flash("Not authenticated")
#             return redirect(request.base_url)
#     return redirect(url_for('creator.my_albums'))
