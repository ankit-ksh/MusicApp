from .extensions import db
from .extensions import login_manager
from flask_login import UserMixin


#Association table for many to many relationship between Playlist and Tracks table
track_playlist = db.Table(
    "track_playlist",
    db.Column("playlist_id", db.ForeignKey("playlist.id"), primary_key=True),
    db.Column("track_id", db.ForeignKey("track.id"), primary_key=True)
)
#Association table for many to many relationship between Track and Creator table
track_creator = db.Table(
    "track_creator",
    db.Column("track_id", db.ForeignKey("track.id"), primary_key=True),
    db.Column("creator_id", db.ForeignKey("creator.id"), primary_key=True)
)
#Association table for many to many relationship between Album and Creator table
album_creator = db.Table(
    "album_creator",
    db.Column("album_id", db.ForeignKey("album.id"), primary_key=True),
    db.Column("creator_id", db.ForeignKey("creator.id"), primary_key=True)
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(10), nullable=False, unique=True)
    first_name = db.Column(db.String(15), nullable=False)
    last_name = db.Column(db.String(15))
    password = db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    ## ----------------------Relationships -------------------------
    #establish relationship with Playlist table
    playlists = db.relationship('Playlist', back_populates='curator', cascade="all, delete")
    
class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    ## ----------------------Relationships -------------------------
    # establish relationship with User table - Many to One
    curator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    curator = db.relationship('User', back_populates='playlists')
    # establish relationshiop with Track table - Many to Many
    tracks = db.relationship('Track', secondary=track_playlist, back_populates='belongs_to')

class Creator(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'))
    creator_id = db.Column(db.Integer, primary_key=True)
    is_flagged = db.Column(db.Boolean, unique=False, default=False)
    ## ----------------------Relationships -------------------------
    # relationship with Track table - Many to Many
    tracks = db.relationship('Track', secondary=track_creator, back_populates='creators')
    # relationship with Album table - Many to Many
    albums = db.relationship('Album', secondary=album_creator, back_populates='creators')

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    is_flagged = db.Column(db.Boolean, unique=False, default=False)
    ## ----------------------Relationships -------------------------
    # relationship with Creator table - Many to Many
    creators = db.relationship('Creator', secondary=album_creator, back_populates='albums')
    # relationship with Track table - One to Many
    tracks = db.relationship('Track', back_populates='album')

class Track(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    times_played = db.Column(db.Integer, default=0)
    genre = db.Column(db.String(10))
    rating = db.Column(db.Float)
    is_flagged = db.Column(db.Boolean, unique=False, default=False)
    ## ----------------------Relationships -------------------------
    # relationship with Creator table - Many to Many
    creators = db.relationship('Creator', secondary=track_creator, back_populates='tracks')
    #relationship with Album table - Many to One
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'))
    album = db.relationship('Album', back_populates='tracks')
    #establish relationshiop with Playlist table - Many to Many
    belongs_to = db.relationship('Playlist', secondary=track_playlist, back_populates='tracks')
    #establish relationship with Lyrics table - One to One
    lyrics = db.relationship('Lyrics', cascade="all, delete")

class Lyrics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lyrics = db.Column(db.String)
    ## ----------------------Relationships -------------------------
    #establishing relationship with Track table
    track_id = db.Column(db.Integer, db.ForeignKey('track.id'), unique=True)
    track = db.relationship('Track', back_populates='lyrics')


