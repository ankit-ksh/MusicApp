from .extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String, nullable=False, unique=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)
    
class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    artist = db.Column()
    path = db.Column(db.String, nullable=False)
    lyrics_path = db.Column(db.String, nullable=False)
    rating = db.Column(db.String)
    cover_image = db.Column(db.String)

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    artist = db.Column(db.String, nullable=False)
    date_created = db.Column(db.String, nullable=False)

class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    creator = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)

# class Association(db.Model):
#     song_id = db.relationship(db.fro)