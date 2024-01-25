# Implementing user pages

from flask import (
    Blueprint, redirect, render_template, request, session, url_for, flash, send_from_directory
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
    return redirect('music/all/tracks')

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



@bp.route('/library')
@login_required
def library():
    tracks = db.session.execute(db.select(Track)).scalars()
    tracks = [track for track in tracks]
    template_data = dict(
        user_rated_items = tracks
    )
    return render_template('general/library.html')

@bp.route('/profile')
@login_required
def profile():
    return render_template('general/profile.html')

@bp.route('/user/become-creator/<int:user_id>')
@login_required
def become_creator(**kwargs):
    user_id = kwargs.get('user_id')
    if user_id:
        user = db.session.get(User, user_id)
        new_creator = Creator(user_name = user.user_name, first_name = user.first_name, last_name=user.last_name, password=user.password)
        db.session.delete(user)
        db.session.commit()
        db.session.add(new_creator)
        db.session.commit()
    template_data = dict(
        message = "You've succesfully registered as a creator. Please login again",
        message_type = 'success'
    )
    return redirect(url_for('general.profile'))


@bp.route('/preferences')
@login_required
def preferences():
    return render_template('general/preferences.html')



@bp.route('/search')
@login_required
def search():
    q = request.args.get('q')
    filtered_by = None
    tracks = None
    filter_by = request.args.get('filter_by')
    if filter_by == 'genre':
        genre_id = request.args.get('genre_id')
        if db.session.get(Genre, genre_id):
            filtered_by = f"Genre : {db.session.get(Genre, genre_id).name}"
            tracks = [result for result in db.session.execute(db.select(Track).where(db.and_(Track.name.ilike(f"%{q}%")), Track.genre_id == genre_id)).scalars()]
            tracks = [track for track in tracks]
    elif filter_by == 'creator':
        creator_id = request.args.get('creator_id')
        if db.session.get(Creator, creator_id):
            filtered_by = f"Creator : {db.session.get(Creator, creator_id).name}"
            tracks = [result for result in db.session.execute(db.select(Track).where(db.and_(Track.name.ilike(f"%{q}%")), Track.creator_id == creator_id)).scalars()]
            tracks = [track for track in tracks]
    elif filter_by == 'language':
        language_id = request.args.get('language_id')
        if db.session.get(Language, language_id):
            filtered_by = f"Language : {db.session.get(Language, language_id).name}"
            tracks = [result for result in db.session.execute(db.select(Track).where(db.and_(Track.name.ilike(f"%{q}%")), Track.language_id == language_id)).scalars()]
            tracks = [track for track in tracks]
    else:
        tracks = [result for result in db.session.execute(db.select(Track).where(Track.name.ilike(f"%{q}%"))).scalars()]
    albums = [result for result in db.session.execute(db.select(Album).where(Album.name.ilike(f"%{q}%"))).scalars()]
    
    # provide genres to select from
    query_result = db.session.execute(db.select(Genre)).scalars()
    all_genres = [genre for genre in query_result]
    # provide creators to select from
    query_result = db.session.execute(db.select(Creator)).scalars()
    all_creators = [creator for creator in query_result]
    # provide Language to select from
    query_result = db.session.execute(db.select(Language)).scalars()
    all_languages = [language for language in query_result]

    template_data = dict(
        tracks = refine_music_data(tracks=tracks).get('tracks'),
        album_results = refine_music_data_cards(content=albums, content_type='album', title=f"Search results for {q} in albums"),
        genres = all_genres,
        creators = all_creators,
        languages = all_languages,
        query_term = q,
        filtered_by = filtered_by
    )
    return render_template('general/search_results.html', **template_data)


@bp.route('/test/<int:test_id>', methods=['GET', 'POST'])
def test(test_id):
    if test_id == 7:
        return send_from_directory('/home/ankit/Music/', 'chori.mp3')
    # return render_template('general/test.html', english_songs=english_songs)
    # return render_template('admin/track_listing.html', english_songs=english_songs)
    template_data = dict(
        message = 'Hello',
        track = db.session.get(Track, 28)
    )
    return render_template(f'test/test_{test_id}.html', **template_data)
