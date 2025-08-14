import os
from flask import Flask
from . import db, auth

def create_app(test_config=None):

    # The instance/ dir is for config data that shouldn't be checked in to git (secret keys, etc)
    # I decided to check in instance/ for this project, for documentation, since it's a tutorial
    # https://flask.palletsprojects.com/en/stable/config/#instance-folders
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite'))
    
    # ensure the instance/ dir exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    if test_config is not None:
        app.config.from_mapping(test_config)
    else:
        app.config.from_pyfile('config.py', silent=True)

    @app.route('/')
    def index():
        return 'Hello, World!'

    db.init_app(app)

    app.register_blueprint(auth.blueprint)

    return app
