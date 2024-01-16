from flask_restful import fields

user_resource_fields = {
    'id' : fields.Integer,
    'user_name' : fields.String,
    'first_name' : fields.String,
    'last_name' : fields.String,
    'role' : fields.String,
}

gnere_name_field = {
    'name' : fields.String
}
creator_name_field = {
    'name' : fields.String
}
album_name_field = {
    'name' : fields.String
}
lyrics_lyrics_field = {
    'language' : fields.String,
    'lyrics' : fields.String
}
track_resource_fields = {
    'id' : fields.Integer,
    'name' : fields.String,
    'artist_name' : fields.String,
    'rating' : fields.Float,
    'release_date' : fields.DateTime,
    'genre' : fields.Nested(gnere_name_field),
    'creator' : fields.Nested(creator_name_field),
    'album' : fields.Nested(album_name_field),
    'lyrics' : fields.Nested(lyrics_lyrics_field)
}
playlist_resource_fields = {
    'id' : fields.Integer,
    'name': fields.String,
    'curator' : fields.Nested(user_resource_fields),
    'tracks' : fields.Nested(track_resource_fields)
}