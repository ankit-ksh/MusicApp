from flask import Flask, Blueprint
from flask_restful import Api, Resource
from sangeet.extensions import api

app = Flask(__name__)
bp = Blueprint('admin_api', __name__)

class SongApi(Resource):
    def get(self):
        return {'task': 'Say "Hello, World!"'}

api.add_resource(SongApi, '/hello')