"""
album_artist_association_table = db.Table('album_to_artist', db.Model.metadata,
                                          db.Column('album_id', db.Integer, db.ForeignKey('album_object.id')),
                                          db.Column('artist_id', db.Integer, db.ForeignKey('artist_object.id')))



artist_track_association_table = db.Table('artist_track', db.Model.metadata,
                                          db.Column('artist_id', db.Integer, db.ForeignKey('artist_object.id')),
                                          db.Column('track_id', db.Integer, db.ForeignKey('track_object.id')))


class ArtistObject(db.Model):
    __tablename__ = "artist_object"

    id = db.Column(db.Integer, primary_key=True)
    # External URL object
    # Followers Object
    # Comma separated list of strings
    genres = db.Column(db.String(120))
    href = db.Column(db.String(80))
    # One to many images relationship
    name = db.Column(db.String(80))
    popularity = db.Column(db.Integer)
    type = db.Column(db.String(6))
    uri = db.Column(db.String(120))

    albums = db.relationship(
        "AlbumObject",
        secondary=album_artist_association_table,
        back_populates='artists')

    tracks = db.relationship(
        "TrackObject",
        secondary=artist_track_association_table,
        back_populates='artists'
    )


class TrackObject(db.Model):
    __tablename__ = "track_object"

    id = db.Column(db.Integer, primary_key=True)
    album_id = db.Column(db.Integer, db.ForeignKey('album_object.id'))
    album = db.relationship('AlbumObject', back_populates="tracks")

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
    audio_features = db.relationship("AudioFeaturesObject", uselist=False, back_populates='track')

    artists = db.relationship(
        "ArtistObject",
        secondary=artist_track_association_table,
        back_populates='tracks'
    )


class AudioFeaturesObject(db.Model):
    __tablename__ = "audio_features"
    id = db.Column(db.Integer, primary_key=True)
    track_id = db.Column(db.Integer, db.ForeignKey('track_object.id'))
    track = db.relationship("TrackObject", uselist=False, back_populates="audio_features")

    acousticness = db.Column(db.Float)
    analysis_url = db.Column(db.String(120))
    danceability = db.Column(db.Integer)
    duration_ms = db.Column(db.Integer)
    energy = db.Column(db.Float)
    instrumentalness = db.Column(db.Float)
    key = db.Column(db.Integer)
    liveness = db.Column(db.Float)
    loudness = db.Column(db.Float)
    mode = db.Column(db.Integer)
    speechiness = db.Column(db.Float)
    tempo = db.Column(db.Float)
    time_signature = db.Column(db.Integer)
    track_href = db.Column(db.String(80))
    uri = db.Column(db.String(120))
    valence = db.Column(db.Float)


class CategoryObject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    href = db.Column(db.String(80))
    # icons - One to many images relationship
    name = db.Column(db.String(30))


class ContextObject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # external_urls - External URL Object
    href = db.Column(db.String(80))
    type = db.Column(db.String(20))
    uri = db.Column(db.String(120))


class CopyRightObject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(80))
    type = db.Column(db.String(10))


class CurrentlyPlayingContextObject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # actions - disallows object
    # context - context object
    currently_playing_type = db.Column(db.String(80))
    # device - Device Object
    is_playing = db.Column(db.Boolean, default=False)
    # item - Track Object
    progress_ms = db.Column(db.Integer)
    repeat_state = db.Column(db.String(80))
    shuffle_state = db.Column(db.String(80))
    timestamp = db.Column(db.Integer)


class CurrentlyPlayingObject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # context - context object (can be null)
    currently_playing_type = db.Column(db.String(20))
    is_playing = db.Column(db.Boolean, default=False)
    # Track Object (can be null)
    progress_ms = db.Column(db.Integer, nullable=True)
    timestamp = db.Column(db.Integer)

"""