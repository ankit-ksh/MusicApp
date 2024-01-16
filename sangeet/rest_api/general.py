from flask import Blueprint, request, jsonify
from sangeet.extensions import api
from sangeet.extensions import db
from sangeet.models import User, Playlist
from flask_restful import Resource, reqparse, marshal_with, marshal
from flask_login import current_user, login_required
from .resource_fields import *
bp = Blueprint('general_api', __name__)


class UserApi(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('user_name')
        self.parser.add_argument('first_name')
        self.parser.add_argument('last_name')
        self.parser.add_argument('password')
        self.parser.add_argument('role')
    @marshal_with(user_resource_fields)
    def get(self, user_id):     # get info about a user
        user = db.session.get(User, user_id)
        return user
    def post(self):    # create a new user, or also create_account for normal user only
        args = self.parser.parse_args()
        if args.get('role') == 'user':
            new_user = User(user_name=args['user_name'], first_name=args['first_name'], last_name=args['last_name'], password=args['password'], role='user')
        elif args.get('role') == 'creator':
            new_user = User(user_name=args['user_name'], first_name=args['first_name'], last_name=args['last_name'], password=args['password'], role='user')
        if new_user.first_name and new_user.password and new_user.user_name:
             new_user_name = new_user.user_name
             already_user_name = db.session.scalar(db.select(User).where(User.user_name == new_user_name))
             if already_user_name:
                  return 'Username already exists. Please try another username'
             pass
        else:
             return 'Either User name, First name or Password was missing'
        db.session.add(new_user)
        db.session.commit()
        return marshal(new_user, user_resource_fields)
    def put(self, user_id):
        args = self.parser.parse_args()
        user_to_update = db.session.get(User, user_id)
        for key, value in args.items():
            if key == 'user_name':
                new_user_name = value
                already_user_name = db.session.scalar(db.select(User).where(User.user_name == new_user_name))
                if already_user_name and (user_to_update.id != already_user_name.id):   # only if a user is trying to set same user id as that of another user
                    return 'Username already exists. Please try another username'
                else:
                        pass
            setattr(user_to_update, key, value)
        db.session.commit()
        return marshal(user_to_update, user_resource_fields)

api.add_resource(UserApi, '/api/user/<int:user_id>', '/api/user/new', '/api/user/update/<int:user_id>')

class PlaylistApi(Resource):
    def __init__(self):
        super().__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('playlist_name')
    def get(self, playlist_id):
        playlist = db.session.get(Playlist, playlist_id)
        return marshal(playlist, playlist_resource_fields)
    
api.add_resource(PlaylistApi, '/api/playlist/<int:playlist_id>', '/api/playlist/new', '/api/playlist/update/<int:playlist_id>')

class TrackApi(Resource):
    def __init__(self):
        super().__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name')
        self.parser.add_argument('artist_name')
        self.parser.add_argument('genre')
        self.parser.add_argument()
