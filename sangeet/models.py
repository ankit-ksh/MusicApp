from .extensions import db

#Association table for many to many relationship between Playlist and Tracks table
track_playlist = db.Table(
    "track_playlist",
    db.Column("playlist_id", db.ForeignKey("playlist.id"), primary_key=True),
    db.Column("track_id", db.ForeignKey("track.id"), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String, nullable=False, unique=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)
    #establish relationship with Playlist table
    playlists = db.relationship('Playlist', back_populates='creator', cascade="all, delete")
    
class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    #establish relationship with User table
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    creator = db.relationship('User', back_populates='playlists')
    #establish relationshiop with Track table
    tracks = db.relationship('Track', secondary=track_playlist, back_populates='belongs_to')

class Creator(User):
    artist_id = db.Column(db.Integer, primary_key=True)
    #establish relationship with User table
    id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #relationship with Track table
    tracks = db.relationship('Track', back_populates='artist')
    #relationship with Album table
    albums = db.relationship('Album', back_populates='artist')

class FlaggedCreator(Creator):
    flagged_creator_id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, db.ForeignKey('creator.id'))
    pass

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    #relationship with Artist table
    artist_id = db.Column(db.Integer, db.ForeignKey('creator.id'))
    artist = db.relationship('Artist', back_populates='albums')
    #_______________________________
    #relationship with Track table
    tracks = db.relationship('Track', back_populates='album')

class FlaggedAlbum(Album):
    flagged_album_id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, db.ForeignKey('album.id'))
    pass


class Track(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    times_played = db.Column(db.Integer, default=0)
    genre = db.Column(db.String)
    rating = db.Column(db.Float)
    #relationship with Artist table
    artist_id = db.Column(db.Integer, db.ForeignKey('creator.id'))
    artist = db.relationship('Artist', back_populates='tracks')
    #relationship with Album table
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'))
    album = db.relationship('Album', back_populates='tracks')
    #establish relationshiop with Playlist table
    belongs_to = db.relationship('Playlist', secondary=track_playlist, back_populates='tracks')
    #establish relationship with Lyrics table
    lyrics = db.relationship('Lyrics', cascade="all, delete")

class FlaggedTrack(Track):
    flagged_track_id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, db.ForeignKey('track.id'))
    pass

class Lyrics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lyrics = db.Column(db.String)
    #establishing relationship with Track table
    track_id = db.Column(db.String, db.ForeignKey('track.id'))
    track = db.relationship('Track', back_populates='lyrics')


