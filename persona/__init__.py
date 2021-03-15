from flask import Flask, request, url_for, redirect, render_template, session
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
import os, json
from .services.twitter.twitter_service import TwitterAuthentication, TwitterAPI
from .services.spotify.spotify_service import SpotifyAuthentication


PATH_TO_CFG = os.path.join("config.json")

def load_config():
    with open(PATH_TO_CFG, 'r') as file:
        return json.load(file)


def save_config_param(service, path, key, value):
    with open(PATH_TO_CFG, 'r') as file:
        cfg = json.load(file)
    cfg['services'][service][path][key] = value
    with open(PATH_TO_CFG, 'w') as file:
        json.dump(cfg, file)


# Create app prior to import anything involving database
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Volumes/Seagate Backup /databases/app.db'
app.debug = True

# Import db from models module. Created in models module to resolve potential circular dependencies
from .models import *


migrate = Migrate(app, db, render_as_batch=True, compare_type=True)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

user = User

# Import routes after app and db has been already created
from .routes.spotify import bp as spotify_bp
from .routes.auth import bp as auth_bp
from .routes.persona import bp as persona_bp
from .routes.twitter import bp as twitter_bp
app.register_blueprint(spotify_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(persona_bp)
app.register_blueprint(twitter_bp)
