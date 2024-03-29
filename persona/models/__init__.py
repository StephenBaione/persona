from persona import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

db = SQLAlchemy(app)

from .spotify_models import Spotify, Image, AlbumObject, ArtistObject, TopArtists, TrackObject, AudioFeatures, TopTracks
from .persona_models import User
from .twitter_models import Twitter, Tweet

# Import both of these modules here so that they are defined when their relationships are established.
# Note: importing these models occured after db was created....... lint will just have to live with that ;)
