from .extensions import db
from .extensions import login_manager
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property


# Association table for many to many relationship between Playlist and Tracks table
track_playlist = db.Table(
    "track_playlist",
    db.Column("playlist_id", db.ForeignKey("playlist.id"), primary_key=True),
    db.Column("track_id", db.ForeignKey("track.id"), primary_key=True)
)
# Association table for many to many relationship between Album and Creator table
user_liked_tracks = db.Table(
    "user_liked_tracks",
    db.Column("user_id", db.ForeignKey('user.id'), primary_key=True),
    db.Column("track_id", db.ForeignKey('track.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(10), nullable=False, unique=True)
    first_name = db.Column(db.String(15), nullable=False)
    last_name = db.Column(db.String(15), default='')
    password = db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    profile_pic_src = db.Column(db.String(50), nullable=True)
    ## ----------------------Relationships -------------------------
    # establish relationship with Playlist table One to Many
    playlists = db.relationship('Playlist', back_populates='curator', cascade="all, delete")
    # establish relationship with Track table for Knowing the likes of a user and also to know about the users who liked a particular song - Many to Many
    liked_tracks = db.relationship('Track', secondary=user_liked_tracks, back_populates='liked_by')
    # to be able to access user.name
    @hybrid_property
    def name(self):
        return f"{self.first_name} {self.last_name}"


    # for a polymorphic relationship
    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': 'role'
    }

class Creator(User):
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    is_blacklisted = db.Column(db.Boolean, unique=False, default=False)
    ## ----------------------Relationships -------------------------
    # relationship with Track table - One to Many
    tracks = db.relationship('Track', back_populates='creator', cascade="all, delete")
    # relationship with Album table - One to Many
    albums = db.relationship('Album', back_populates='creator', cascade="all, delete")

    # polymorphic identity of creator
    __mapper_args__ = {"polymorphic_identity": "creator"}

class Admin(User):
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    # polymorphic identity of admin
    __mapper_args__ = {"polymorphic_identity": "admin"}

class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    is_public = db.Column(db.Boolean, unique=False, default=True)
    ## ----------------------Relationships -------------------------
    # establish relationship with User table - Many to One
    curator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    curator = db.relationship('User', back_populates='playlists')
    # establish relationshiop with Track table - Many to Many
    tracks = db.relationship('Track', secondary=track_playlist, back_populates='belongs_to_playlist')

class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    ## ----------------------Relationships -------------------------
    # relationship with Track table - One to many
    tracks = db.relationship('Track', back_populates='artist')
    # relationship with Album Table - One to many
    albums = db.relationship('Album', back_populates='artist')

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    genre_id = db.Column(db.Integer)
    release_date = db.Column(db.DateTime, default=datetime.now(), nullable=True)
    is_flagged = db.Column(db.Boolean, unique=False, default=False)
    description = db.Column(db.String)
    ## ----------------------Relationships -------------------------
    # relationship with Creator table - Many to one
    creator_id = db.Column(db.Integer, db.ForeignKey('creator.creator_id'))
    creator = db.relationship('Creator', back_populates='albums')
    # relationship with Track table - One to Many
    tracks = db.relationship('Track', back_populates='album', cascade="all, delete")
    # establish relationship with Language table - Many to One
    language_id = db.Column(db.Integer, db.ForeignKey('language.id'))
    language = db.relationship('Language')
    # establsh relationship with Genre  - Many to One
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'))
    genre = db.relationship('Genre', back_populates='albums')
    # establish relationship with Artist - Many to One
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
    artist = db.relationship('Artist', back_populates='albums')


class Track(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    file_name = db.Column(db.String, nullable=False)
    artist_name = db.Column(db.String(40), nullable=False)
    times_played = db.Column(db.Integer, default=0)
    rating = db.Column(db.Float, default=0, index=True)
    is_flagged = db.Column(db.Boolean, unique=False, default=False)
    file_path = db.Column(db.String(200), default='#')
    upload_date = db.Column(db.DateTime, default=datetime.now())
    release_date = db.Column(db.DateTime, default=datetime.now())
    duration = db.Column(db.String)
    ## ----------------------Relationships -------------------------
    # relationship with Genre table - Many to One
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), nullable=True)
    genre = db.relationship('Genre', back_populates='tracks')
    # relationship with Creator table - Many to One
    creator_id = db.Column(db.Integer, db.ForeignKey('creator.creator_id'))
    creator = db.relationship('Creator', back_populates='tracks')
    #relationship with Album table - Many to One
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'), nullable=True)
    album = db.relationship('Album', back_populates='tracks')
    # establish relationshiop with Playlist table - Many to Many
    belongs_to_playlist = db.relationship('Playlist', secondary=track_playlist, back_populates='tracks')
    # establish relationship with Lyrics table - One to One
    lyrics = db.relationship('Lyrics', cascade="all, delete")
    # establish relationship with Language table - Many to One
    language_id = db.Column(db.Integer, db.ForeignKey('language.id'), nullable=True)
    language = db.relationship('Language')
    # establish relationship with Track table for Knowing the likes of a user and also to know about the users who liked a particular song - Many to Many
    liked_by = db.relationship('User', secondary=user_liked_tracks, back_populates='liked_tracks')
    # establish relationship with Artist - Many to One
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
    artist = db.relationship('Artist', back_populates='tracks')

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    ## ----------------------Relationships -------------------------
    # establish relationship with Track table - One to Many
    tracks = db.relationship('Track', back_populates='genre')
    # establish relationship with Album table - One to Many
    albums = db.relationship('Album', back_populates='genre')
    

class Lyrics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lyrics = db.Column(db.String)
    rating = db.Column(db.Float, default=0)
    ## ----------------------Relationships -------------------------
    # establishing relationship with Track table - Many to One
    track_id = db.Column(db.Integer, db.ForeignKey('track.id'), nullable=True)
    track = db.relationship('Track', back_populates='lyrics')
    # establishing relationship with Language table - Many to One
    language_id = db.Column(db.Integer, db.ForeignKey('language.id'), nullable=True)
    language = db.relationship('Language')

class Language(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(12), nullable=False, unique=True)
    ## ----------------------Relationships -------------------------
    # establishing relationship with Track table - One to Many
    tracks = db.relationship('Track', back_populates='language')
    # establishing relationship with Album table - One to Many
    albums = db.relationship('Album', back_populates='language')

