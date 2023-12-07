# Implementing creator pages

from flask import (
    Blueprint, redirect, render_template, request, session, url_for
)
from sangeet.extensions import db
from flask_login import (
    login_user,
    logout_user,
    login_required,
)

bp = Blueprint('creator', __name__)


@bp.route('/creator/dashboard')
def dashboard():
    return render_template('creator/dashboard.html')


@bp.route('/my_content/songs')
def my_songs():
    return render_template('creator/my_songs.html')

@bp.route('/my_content/albums')
def my_albums():
    return render_template('creator/my_songs.html')


@bp.route('/upload/song')
def upload_song():
    return render_template('creator/upload_song.html')

@bp.route('/create/album')
def create_album():
    return render_template('creator/create_album.html')

