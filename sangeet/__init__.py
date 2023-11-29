import os
from flask import Flask
from .extensions import db



def create_app(test_config=None):
    # creating the flask app as an instance of the Flask Class
    app = Flask(__name__, instance_relative_config=True)

    # ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # initialising database, if required
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sangeet.sqlite3"
    db.init_app(app)
    from . import models
    with app.app_context():
        db.create_all()

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

    return app
