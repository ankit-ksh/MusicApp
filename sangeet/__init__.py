import os
from flask import Flask
from .extensions import db
from .extensions import login_manager
# Followig import is for getting the user object for the user loader of flask login LoginManager
from sangeet.models import User



def create_app(test_config=None):
    # creating the flask app as an instance of the Flask Class
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI = "sqlite:///sangeet.sqlite3",
    )


    # ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # initialising database, if required
    db.init_app(app)
    from . import models
    with app.app_context():
        db.create_all()

    # configuring flask login
    login_manager.init_app(app)
    #loading the user
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))


    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    
    # registering the blueprints
    from .views import auth
    app.register_blueprint(auth.bp)
    from .views import user
    app.register_blueprint(user.bp)
    from .views import creator
    app.register_blueprint(creator.bp)
    from .views import admin
    app.register_blueprint(admin.bp)


    return app
