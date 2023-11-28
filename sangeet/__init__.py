import os
from flask import Flask



def create_app(test_config=None):
    # creating the flask app as an instance of the Flask Class
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='sec',
        DATABASE=os.path.join(app.instance_path, 'sangeet.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)


    # ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # registering the user blueprint
    from .views import auth
    app.register_blueprint(auth.bp)

    return app
