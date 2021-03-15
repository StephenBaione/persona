from . import db
from sqlalchemy import func

spotify_to_saved_tracks_association_table = db.Table("spotify_to_saved_tracks", db.Model.metadata,
                                                     db.Column('spotify_id', db.Integer, db.ForeignKey('spotify.id')),
                                                     db.Column('track_id', db.String(80),
                                                               db.ForeignKey('track_object.id')))


class Spotify(db.Model):
    __tablename__ = 'spotify'

    # ---- User Information ----
    id = db.Column(db.Integer, primary_key=True)
    display_name = db.Column(db.String(80))
    country = db.Column(db.String(20))
    email = db.Column(db.String(40), nullable=True)
    # Link to web API endpoint for user
    href = db.Column(db.String(80))
    # user's subscription level
    product = db.Column(db.String(15))
    # Spotify uri for user
    uri = db.Column(db.String(80))
    # Number of followers
    followers = db.Column(db.Integer())
    type = db.Column(db.String(20))

    # Explicit content settings
    filter_enabled = db.Column(db.Boolean(), default=False)
    filter_locked = db.Column(db.Boolean(), default=False)

    # External Url
    external_urls = db.Column(db.String(200))

    # ---- Relationships ----
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', uselist=False, back_populates='spotify')
    images = db.relationship("Image")
    top_artists = db.relationship("TopArtists", backref='spotify', lazy=True)
    top_tracks = db.relationship("TopTracks", backref='spotify', lazy=True)
    listening_session = db.relationship("ListeningSession", backref='spotify', lazy=True)
    saved_tracks = db.relationship("TrackObject",
                                   secondary=spotify_to_saved_tracks_association_table,
                                   back_populates="saved_spotify")

    # ---- Token Object ----
    access_token = db.Column(db.String(80))
    token_type = db.Column(db.String(20))
    expires_at = db.Column(db.Integer())
    refresh_token = db.Column(db.String(80))
    scopes = db.Column(db.String(80))

    def __init__(self, **kwargs):
        self.display_name = kwargs.get('display_name')
        self.country = kwargs.get('country')
        self.email = kwargs.get('email', None)
        self.href = kwargs.get('href')
        product = kwargs.get('product')
        if product == "open":
            product = "free"
        self.product = product
        self.uri = kwargs.get('uri')
        self.followers = kwargs.get('followers')
        self.filter_enabled = kwargs.get('filter_enabled')
        self.filter_locked = kwargs.get('filter_locked')
        self.external_url = kwargs.get('external_url')
        self.user = kwargs.get('user')
        # Assuming each image is passed in as dictionary object
        images = kwargs.get('images')
        if images is not None:
            for image in images:
                url = image['url']
                height = image.get('height', None)
                width = image.get('width', None)
                image_object = Image(url=url, height=height, width=width)
                self.images.append(image_object)
        token = kwargs.get("token")
        if token is not None:
            self.access_token = token.get('access_token')
            self.token_type = token.get('token_type')
            self.expires_at = token.get('expires_at')
            self.refresh_token = token.get('refresh_token')
            self.scopes = token.get('scopes')
        else:
            self.access_token = None
            self.token_type = None
            self.expires_at = None
            self.refresh_token = None
            self.scopes = None

    def create(self, data):
        new_spotify = Spotify(**data)
        db.session.add(new_spotify)
        db.session.commit()

    def read(self, spotify_id):
        return self.query.filter_by(id=spotify_id)

    def update(self, data: dict):
        for field, value in data.items():
            self.__setattr__(field, value)

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Image(db.Model):
    __tablename__ = "spotify_image"
    url = db.Column(db.String(80), primary_key=True)
    height = db.Column(db.Integer(), nullable=True)
    width = db.Column(db.Integer(), nullable=True)
    spotify_relationship = db.Column(db.Integer(), db.ForeignKey('spotify.id'))
    album_relationship = db.Column(db.Integer(), db.ForeignKey('album_object.id'))
    artist_relationship = db.Column(db.Integer(), db.ForeignKey('artist_object.id'))


album_artist_association_table = db.Table('album_to_artist', db.Model.metadata,
                                          db.Column('album_id', db.String, db.ForeignKey('album_object.id')),
                                          db.Column('artist_id', db.String, db.ForeignKey('artist_object.id')))


class AlbumObject(db.Model):
    __tablename__ = "album_object"

    id = db.Column(db.String(80), primary_key=True)
    album_type = db.Column(db.String(80))
    # Comma seperated string representing array
    available_markets = db.Column(db.String(200))
    # One to many Copyrights relationship
    # External ID object
    # External url object
    # Comma seperated string representing array
    genres = db.Column(db.String(200))
    href = db.Column(db.String(80))
    image = db.relationship("Image")
    label = db.Column(db.String(80))
    popularity = db.Column(db.Integer)
    release_date = db.Column(db.String(80))
    release_date_precision = db.Column(db.String(20))
    album_restriction_reason = db.Column(db.String(20))
    # tracks = db.relationship("TrackObject", back_populates="album")
    type = db.Column(db.String(20))
    uri = db.Column(db.String(80))

    # -------- Relationships --------
    artists = db.relationship(
        "ArtistObject",
        secondary=album_artist_association_table,
        back_populates="albums"
    )

    def __init__(self, **data):
        self.id = data['id']
        self.album_type = data['album_type']
        self.available_markets = ','.join(data['available_markets'])[:200]
        self.genres = ','.join(data['genres'])
        images = data.get("images", None)
        if images is not None:
            for image in images:
                url = image['url']
                height = image.get('height', None)
                width = image.get('width', None)
                image_object = Image(url=url, height=height, width=width)
                self.image.append(image_object)
        self.label = data['label']
        self.popularity = data['popularity']
        self.release_date = data['release_date']
        self.release_date_precision = data['release_date_precision']
        self.album_restriction_reason = data.get("album_restriction_reason", None)
        self.type = data['type']
        self.uri = data['uri']
        # Artists should have been created or loaded in model handler
        artists = data['artists']
        for artist in artists:
            self.artists.append(artist)


artist_to_top_artists_table = db.Table("artists_to_top_artists", db.Model.metadata,
                                       db.Column('artist_id', db.String(80), db.ForeignKey('artist_object.id')),
                                       db.Column('top_artists_id', db.Integer, db.ForeignKey('top_artists.id')))

artist_track_association_table = db.Table('artist_track', db.Model.metadata,
                                          db.Column('artist_id', db.String, db.ForeignKey('artist_object.id')),
                                          db.Column('track_id', db.String, db.ForeignKey('track_object.id')))


class ArtistObject(db.Model):
    __tablename__ = "artist_object"

    id = db.Column(db.String(80), primary_key=True)
    # External URL object
    # Followers Object
    # Comma separated list of strings
    genres = db.Column(db.String(120))
    href = db.Column(db.String(80))
    # One to many images relationship
    image = db.relationship("Image")
    name = db.Column(db.String(80))
    popularity = db.Column(db.Integer)
    type = db.Column(db.String(6))
    uri = db.Column(db.String(120))

    # -------- Relationships --------
    # Many to Many
    albums = db.relationship(
        "AlbumObject",
        secondary=album_artist_association_table,
        back_populates='artists')

    top_artists = db.relationship(
        "TopArtists",
        secondary=artist_to_top_artists_table,
        back_populates='artists')

    tracks = db.relationship(
        "TrackObject",
        secondary=artist_track_association_table,
        back_populates='artists'
    )

    def __init__(self, **data):
        self.id = data['id']
        self.genres = ','.join(data['genres'])
        self.href = data['href']
        images = data.get("images", None)
        if images is not None:
            for image in images:
                url = image['url']
                height = image.get('height', None)
                width = image.get('width', None)
                image_object = Image(url=url, height=height, width=width)
                self.image.append(image_object)
        self.name = data['name']
        self.popularity = data['popularity']
        self.type = data['type']
        self.uri = data['uri']


class TopArtists(db.Model):
    __tablename__ = "top_artists"

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime(timezone=True), server_default=func.now())

    # -------- Relationships --------
    # Many to Many
    artists = db.relationship(
        "ArtistObject",
        secondary=artist_to_top_artists_table,
        back_populates='top_artists')

    # One to Many
    spotify_id = db.Column(db.Integer, db.ForeignKey('spotify.id'), nullable=True)

    def add_artist(self, artist_object):
        self.artists.append(artist_object)


track_to_top_tracks_table = db.Table("track_to_top_tracks", db.Model.metadata,
                                     db.Column('track_id', db.String(80), db.ForeignKey('track_object.id')),
                                     db.Column('top_tracks_id', db.Integer, db.ForeignKey('top_tracks.id')))

tracks_to_listening_session_table = db.Table("track_to_listening_session", db.Model.metadata,
                                             db.Column('track_id', db.String(80), db.ForeignKey('track_object.id')),
                                             db.Column('listening_session_id', db.Integer, db.ForeignKey('listening_session.id')))


class TrackObject(db.Model):
    __tablename__ = "track_object"

    id = db.Column(db.String(80), primary_key=True)
    album_id = db.Column(db.Integer, db.ForeignKey('album_object.id'))
    # album = db.relationship('AlbumObject', back_populates="tracks")

    # comma separated string
    available_markets = db.Column(db.String(200))
    disc_number = db.Column(db.Integer)
    duration_ms = db.Column(db.Integer)
    explicit = db.Column(db.Boolean)
    # external id object
    # external url object
    href = db.Column(db.String(80))
    is_local = db.Column(db.Boolean, default=False)
    is_playable = db.Column(db.Boolean, default=True)
    name = db.Column(db.String(80))
    popularity = db.Column(db.Integer)
    preview_url = db.Column(db.String(120))
    # track restriction object
    track_number = db.Column(db.Integer)
    type = db.Column(db.String(20))
    uri = db.Column(db.String(80))

    # -------- Relationships --------
    audio_features = db.relationship("AudioFeatures", uselist=False, back_populates='track')
    artists = db.relationship(
        "ArtistObject",
        secondary=artist_track_association_table,
        back_populates='tracks'
    )
    top_tracks = db.relationship(
        "TopTracks",
        secondary=track_to_top_tracks_table,
        back_populates='tracks')

    saved_spotify = db.relationship("Spotify",
                                    secondary=spotify_to_saved_tracks_association_table,
                                    back_populates="saved_tracks")

    def __init__(self, **kwargs):
        self.id = kwargs.get("id", None)
        self.album_id = kwargs.get("album_id", None)
        available_markets = kwargs.get('available_markets', None)
        if available_markets is not None:
            available_markets = ','.join(available_markets)
        self.available_markets = available_markets
        self.disc_number = kwargs.get("disc_number", None)
        self.duration_ms = kwargs.get("duration_ms", None)
        self.explicit = kwargs.get("explicit", None)
        self.href = kwargs.get("href", None)
        self.is_local = kwargs.get("is_local", None)
        self.is_playable = kwargs.get("is_playable", None)
        self.name = kwargs.get("name", None)
        self.popularity = kwargs.get("popularity", None)
        self.preview_url = kwargs.get("preview_url", None)
        self.track_number = kwargs.get("track_number", None)
        self.type = kwargs.get("type", None)
        self.uri = kwargs.get("uri", None)

    def toJson(self):
        return {
            "id": self.id,
            "album_id": self.album_id,
            "available_markets": self.available_markets,
            "disc_number": self.disc_number,
            "duration_ms": self.duration_ms,
            "explicit": self.explicit,
            "href": self.href,
            "is_local": self.is_local,
            "is_playable": self.is_playable,
            "name": self.name,
            "popularity": self.popularity,
            "preview_url": self.preview_url,
            "track_number": self.track_number,
            "type": self.type,
            "uri": self.uri
        }


class TopTracks(db.Model):
    __tablename__ = "top_tracks"

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime(timezone=True), server_default=func.now())

    # -------- Relationships --------
    # Many to Many
    tracks = db.relationship(
        "TrackObject",
        secondary=track_to_top_tracks_table,
        back_populates="top_tracks"
    )

    spotify_id = db.Column(db.Integer, db.ForeignKey('spotify.id'), nullable=True)

    def add_track(self, track_object):
        self.tracks.append(track_object)


class ListeningSession(db.Model):
    __tablename__ = "listening_session"

    id = db.Column(db.Integer, primary_key=True)
    timestamp_begin = db.Column(db.DateTime(timezone=True))
    timestamp_end = db.Column(db.DateTime(timezone=True))

    # -------- Relationships --------
    tracks = db.relationship(
        "TrackObject",
        secondary=tracks_to_listening_session_table)
    spotify_id = db.Column(db.Integer, db.ForeignKey('spotify.id'), nullable=True)


class AudioFeatures(db.Model):
    __tablename__ = "audio_features"

    id = db.Column(db.String(80), primary_key=True)
    type = db.Column(db.String(20))
    uri = db.Column(db.String(120))
    track_href = db.Column(db.String(120))
    analysis_url = db.Column(db.String(120))

    # Analysis Features
    danceability = db.Column(db.Float)
    energy = db.Column(db.Float)
    key = db.Column(db.Integer)
    loudness = db.Column(db.Float)
    speechiness = db.Column(db.Float)
    acousticness = db.Column(db.Float)
    instrumentalness = db.Column(db.Float)
    liveness = db.Column(db.Float)
    valence = db.Column(db.Float)
    tempo = db.Column(db.Float)
    duration_ms = db.Column(db.Integer)
    time_signature = db.Column(db.Integer)

    # -------- Relationships --------
    track_id = db.Column(db.Integer, db.ForeignKey('track_object.id'))
    track = db.relationship("TrackObject", back_populates='audio_features')

    def __init__(self, track: TrackObject, **kwargs):
        self.track = track
        self.id = kwargs.get("id", None)
        self.type = kwargs.get("type", None)
        self.uri = kwargs.get("uri", None)
        self.track_href = kwargs.get("track_href", None)
        self.analysis_url = kwargs.get("analysis_url", None)
        self.danceability = kwargs.get("danceability", None)
        self.energy = kwargs.get("energy", None)
        self.key = kwargs.get("key", None)
        self.loudness = kwargs.get("loudness", None)
        self.speechiness = kwargs.get("speechiness", None)
        self.acousticness = kwargs.get("acousticness", None)
        self.instrumentalness = kwargs.get("instrumentalness", None)
        self.liveness = kwargs.get("liveness", None)
        self.valence = kwargs.get("valence", None)
        self.tempo = kwargs.get("tempo", None)
        self.duration_ms = kwargs.get("duration_ms", None)
        self.time_signature = kwargs.get("time_signature", None)
