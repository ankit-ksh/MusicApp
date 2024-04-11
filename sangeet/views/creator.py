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
from sangeet.utils.general import *
from sangeet.utils.decorators import *

bp = Blueprint('creator', __name__, static_folder='static')

@bp.route('/creator/dashboard/<int:creator_id>')
@creator_required
def dashboard(creator_id):
    my_data = dict(
        track = {'total_in_number': len(current_user.tracks)},
        album = {'total_in_number': len(current_user.albums)},
    )
    template_data = dict(
        my_data = my_data
    )
    return render_template('creator/dashboard.html', **template_data)


@bp.route('/track/upload', methods=['GET', 'POST'])
@creator_required
def upload_track():
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

            # get file duration
            try:
                str_fp = str(filepath)
                duration = get_file_duration(str_fp)
            except:
                duration = ''

            # Save file information to the database
            new_track = Track(name=track_title, artist_name=artist_name, creator_id=creator_id, genre_id=genre_id, file_name=filename, file_path=filepath, duration=duration)
            db.session.add(new_track)
            db.session.commit()
            # save lyrics
            user_sent_lyrics = request.form.get('lyrics')
            new_lyrics = Lyrics(lyrics=user_sent_lyrics, track_id=new_track.id)
            db.session.add(new_lyrics)
            db.session.commit()
            return redirect(url_for('creator.my_content', resource='tracks'))
        else:
            flash('Failed', 'error')
            return 'failed'
    # provide genres to select from
    query_result = db.session.execute(db.select(Genre)).scalars()
    genres = [genre for genre in query_result]
    return render_template('creator/upload_track.html', genres=genres)


@bp.route('/track/<action>', methods=['GET', 'POST'])
@original_creator_required
def modify_track(**kwargs):
    if kwargs.get('action') == 'edit':
        if request.method == 'GET':
            track_id = request.args.get('track_id')
            if track_id:
                # provide genres to select from
                genre_query_result = db.session.execute(db.select(Genre)).scalars()
                template_data = dict(
                    track = db.session.get(Track, track_id),
                    genres = [genre for genre in genre_query_result]
                )
                return render_template('creator/edit_track.html', **template_data)
            else:
                return redirect(request.referrer)
        # post method edit action
        if request.method == 'POST':
            track_id = request.form.get('track_id')
            track_to_edit = db.session.get(Track, track_id)
            # return request.form

            # print(track_to_edit.name)
            # setattr(track_to_edit, 'track_title', )
            
            for key, value in request.form.items():
                if (key not in ['lyrics', 'file']) and (value not in ['None', '', None]):
                    print(key, value)
                    setattr(track_to_edit, key, value)
            file = request.files.get('file', None)
            # for handling the actual file
            if file:
                filename = secure_filename(file.filename)
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

                # create folder if it doesn't exist
                os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
                # Save file to the file system
                file.save(filepath)

                # get file duration
                try:
                    str_fp = str(filepath)
                    duration = get_file_duration(str_fp)
                except:
                    duration = ''
                setattr(track_to_edit, 'file_name', filename)
                setattr(track_to_edit, 'file_path', filepath)
                setattr(track_to_edit, 'duration', duration)
            # for handling lyrics
            user_sent_lyrics = request.form.get('lyrics')
            if track_to_edit.lyrics:
                old_lyrics = track_to_edit.lyrics[0]
                old_lyrics.lyrics = user_sent_lyrics
            else:
                new_lyrics = Lyrics(lyrics=user_sent_lyrics, track_id=track_id)
                db.session.add(new_lyrics)
            # iterate through the post data to update track_to_update
            try:
                db.session.add(track_to_edit)
                db.session.commit()
                return redirect(url_for('creator.my_content', resource='tracks'))
            except:
                return redirect(url_for('creator.my_content', resource='tracks'))
    if kwargs.get('action') == 'delete':
        track_id = request.args.get('track_id')
        if not track_id:
            return redirect(request.referrer)
        track_to_delete = db.session.get(Track, track_id)
        if track_to_delete:
            try:
                track_name = track_to_delete.name
                db.session.delete(track_to_delete)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
        else:
            flash("Not authenticated")
        return redirect(request.referrer)
    else:
        return redirect(request.referrer)
    
@bp.route('/album/create', methods=['GET', 'POST'])
@creator_required
def create_album():
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
        return redirect(url_for('music.overview_of_category', category='album', category_id=new_album.id))
    query_result = db.session.execute(db.select(Genre)).scalars()
    genres = [genre for genre in query_result]
    template_data = dict(
        genres = genres
    )
    return render_template('creator/create_album.html', **template_data)


# any action related to albums which modifies it
@bp.route('/album/<action>', methods=['GET', 'POST'])    
@original_creator_required
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
    elif action == 'delete':
        db.session.delete(album)
        db.session.commit()
    return redirect(request.referrer)

@bp.route('/my-content/<resource>')
@creator_required
def my_content(**kwargs):
    if kwargs.get('resource') == 'tracks':
        template_data = dict(
            tracks = refine_music_data(tracks=current_user.tracks)['tracks'],
            music_collection = refine_music_data(music_collection=current_user)['music_collection'],
            main_category = 'creator'
        )
        return render_template('music/real_music_overview_page.html', **template_data)
    elif kwargs.get('resource') == 'albums':
        content_type='album'
        music_data = refine_music_data_cards(content_type = content_type, owner_id=current_user.id)
        template_data = dict(
            main_category = 'creator', # for sending the user to show all page - link buildup
            content = music_data['content'],
            links = music_data['links'],
            title = 'My Albums',
            content_type = content_type,
            music_data = music_data
        )
        return render_template('music/music_display_cards.html', **template_data)
    else:
        return redirect(request.referrer)

