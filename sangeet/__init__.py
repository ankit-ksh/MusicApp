import os
from flask import Flask
from flask_login import current_user
from sangeet.extensions import db
from sangeet.extensions import login_manager
from sangeet.extensions import api
# Following import is for getting the user object for the user loader of flask login LoginManager
from sangeet.models import User
# To register all api resources I need it all in this file so I need to import all the api blueprints outside the api function
# for the normal web app functionality, it works even when being inside a function, but for APIs I'll have to keep it inside
from sangeet.rest_api import general as general_api
from sangeet.rest_api import admin as admin_api
from sangeet.rest_api import creator as creator_api
from sangeet.views import auth, general, creator, admin, music, playlist


def create_app(test_config=None):
    # creating the flask app as an instance of the Flask Class
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI = "sqlite:///sangeet.sqlite3",
        SQLALCHEMY_TRACK_MODIFICATIONS = True, # False in production to increase performance, True in development for reloading without restarting the server
        # TEMPLATES_AUTO_RELOAD = True
        UPLOAD_FOLDER = "sangeet/static/user_data/track_uploads"
    )

    # ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # initialising database, if required
    db.init_app(app)
    # from . import models
    with app.app_context():
        db.create_all()

    # Intialising and configuring flask login
    login_manager.init_app(app)
    #loading the user
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))
    
    # Intialising and configuring Flask Restful
    api.init_app(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    

    # registering the context processors
    from .utils.configuration import inject_user_based_data
    app.context_processor(inject_user_based_data)

    # registering the blueprints - for web application
    app.register_blueprint(auth.bp)
    app.register_blueprint(general.bp)
    app.register_blueprint(creator.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(music.bp)
    app.register_blueprint(playlist.bp)

    # registering API blurprints
    app.register_blueprint(general_api.bp)
    app.register_blueprint(admin_api.bp)
    app.register_blueprint(creator_api.bp)


    return app

