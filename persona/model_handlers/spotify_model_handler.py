from . import db
from . import User, Spotify, ArtistObject, TopArtists, AlbumObject, TrackObject, AudioFeatures, TopTracks
from . import persona_model_handler
from persona.services.spotify import spotify_service

"""
For each database model implement:
    Create - Create a new database object
    Read - Read or 'load' a database object
    Update - Update field(s) for the object
    Delete - Delete an object from database

TODO:// The following functionality
If a short model shows up in an object (for example, an album that has not been stored to the database yet within a 
track object, then we need to request that Album from the spotify service and save it, then complete the storing
of the Track object.
"""
# -------- Spotify Object --------


# Create
def create_spotify_object_from_json(user_id, data: dict):
    if check_if_spotify_exists(user_id):
        return False
    persona_user = persona_model_handler.load_user("id", user_id)
    country = data['country']
    display_name = data['display_name']
    email = data['email']
    explicit_content = data['explicit_content']
    filter_enabled = explicit_content['filter_enabled']
    filter_locked = explicit_content['filter_locked']
    external_urls_dict = data['external_urls']
    external_urls = ''
    for key, val in external_urls_dict.items():
        external_urls += f"{key}={val},"
    external_urls = external_urls[:-1]
    followers = data['followers']['total']
    href = data['href']
    images = data['images']
    product = data['product']
    type = data['type']
    uri = data['uri']
    token = data["token"]

    kwargs = {
        "country": country,
        "display_name": display_name,
        "email": email,
        "filter_enabled": filter_enabled,
        "filter_locked": filter_locked,
        "external_urls": external_urls,
        "followers": followers,
        "href": href,
        "images": images,
        "product": product,
        "type": type,
        "uri": uri,
        "user": persona_user,
        "token": token
    }
    spotify = Spotify(**kwargs)
    try:
        db.session.add(spotify)
        persona_user.spotify_connected = True
        db.session.commit()
        return True
    except Exception as e:
        print("Error adding spotify object to database\n")
        print(e)
        return True


# Read
def check_if_spotify_exists(user_id):
    spotify = Spotify.query.filter_by(id=user_id).first()
    if spotify is None:
        return False
    return True


def load_object_from_user_id(user_id):
    return Spotify.query.filter_by(user_id=user_id).first()


def load_auth_token(user_id):
    sp = Spotify.query.filter_by(user_id=user_id).first()
    access_token = sp.access_token
    token_type = sp.token_type
    expires_at = sp.expires_at
    refresh_token = sp.refresh_token
    scopes = sp.scopes
    return {
        "access_token": access_token,
        "token_type": token_type,
        "expires_at": expires_at,
        "refresh_token": refresh_token,
        "scopes": scopes
    }


# Update
def update_spotify_object_from_json(user_id, data: dict):
    sp_object = load_object_from_user_id(user_id)
    if sp_object is not None:
        for field, value in data.items():
            sp_object.__setattr__(field, value)
        db.session.commit()
        return True
    return False


# -------- Album --------
def create_album_object_from_json(data):
    artists = data['artists']
    artist_objects = []
    for artist in artists:
        create_artist_object_from_json(artist)
        artist_object = load_artist_by_id(artist['id'])
        artist_objects.append(artist_object)
    data['artists'] = artist_objects
    AlbumObject(**data)


def load_album_by_id(album_id):
    return AlbumObject.query.filter_by(id=album_id).first()


def check_if_album_exists(album_id):
    if load_album_by_id(album_id) is not None:
        return True
    return False


def update_album(album_id, data: dict):
    album = load_album_by_id(album_id)
    if album is not None:
        for field, value in data.items():
            album.__setattr__(field, value)
        db.session.commit()
        return True
    return False


def delete_album(album_id):
    album = load_album_by_id(album_id)
    if album is not None:
        db.session.delete(album)
        db.session.commit()
        return True
    return False


# -------- Artist --------
def create_artist_object_from_json(data):
    if not check_if_artist_exists(data['id']):
        try:
            new_artist = ArtistObject(**data)
            db.session.add(new_artist)
            db.session.commit()
            return True

        except Exception as e:
            print(e)
    return False


def load_artist_by_id(artist_id):
    return ArtistObject.query.filter_by(id=artist_id).first()


def check_if_artist_exists(artist_id):
    results = ArtistObject.query.filter_by(id=artist_id).first()
    if results is None:
        return False
    return True


def update_artist_object(artist_id, data: dict):
    artist = load_artist_by_id(artist_id)
    if artist is not None:
        try:
            for field, value in data.items():
                artist.__setattr__(field, value)
            db.session.commit()
            return True

        except Exception as e:
            print(e)
    return False


# -------- Top Artist --------
def create_top_artists(spotify_object, artists: list):
    top_artists = TopArtists()
    try:
        for artist in artists:
            if not check_if_artist_exists(artist['id']):
                create_artist_object_from_json(artist)
            artist_object = load_artist_by_id(artist['id'])
            top_artists.add_artist(artist_object)
        spotify_object.top_artists.append(top_artists)
        db.session.add(top_artists)
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False


def load_top_artists(top_artist_id):
    return TopArtists.query.filter_by(id=top_artist_id)


def check_if_top_artists_exists(top_artist_id):
    if load_top_artists(top_artist_id) is not None:
        return True
    return False


def update_top_artists(top_artist_id, data: dict):
    top_artists = load_top_artists(top_artist_id)
    if top_artists is not None:
        for field, value in data.items():
            top_artists.__setattr__(field, value)
        db.session.commit()
        return True
    return False


def delete_top_artists(top_artist_id):
    top_artists = load_top_artists(top_artist_id)
    if top_artists is not None:
        db.session.delete(top_artists)
        db.session.commit()
        return True
    return False


# -------- Tracks --------
def create_track_object(track: dict):
    if not check_if_track_exists(track['id']):
        try:
            track_object = TrackObject(**track)
            db.session.add(track_object)
            db.session.commit()
        except Exception as e:
            print(e)


def create_track_object_batch(tracks):
    for track in tracks:
        if not check_if_track_exists(track['id']):
            try:
                track_object = TrackObject(**track)
                db.session.add(track_object)
            except Exception as e:
                print(e)
        else:
            print("Track already exists")
    db.session.commit()


def load_track_object(track_id):
    return TrackObject.query.filter_by(id=track_id).first()


def check_if_track_exists(track_id):
    if load_track_object(track_id) is not None:
        return True
    return False


def update_track(track_id, data):
    track = load_track_object(track_id)
    if track is not None:
        for field, value in data:
            track.__setattr__(field, value)
        db.session.commit()
        return True
    return False


def delete_track(track_id):
    track = load_track_object(track_id)
    if track is not None:
        db.session.delete(track)
        db.session.commit()
        return True
    return False


# -------- Top Tracks --------
def create_top_tracks(spotify_object, tracks: list):
    top_tracks = TopTracks()
    try:
        for track in tracks:
            if not check_if_track_exists(track['id']):
                create_artist_object_from_json(track)
            artist_object = load_artist_by_id(track['id'])
            top_tracks.add_artist(artist_object)
        spotify_object.top_tracks.append(top_tracks)
        db.session.add(top_tracks)
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False


def load_top_tracks(top_track_id):
    return TopTracks.query.filter_by(id=top_artist_id)


def check_if_top_tracks_exists(top_track_id):
    if load_top_tracks(top_track_id) is not None:
        return True
    return False


def update_top_tracks(top_track_id, data: dict):
    top_tracks = load_top_tracks(top_track_id)
    if top_tracks is not None:
        for field, value in data.items():
            top_tracks.__setattr__(field, value)
        db.session.commit()
        return True
    return False


def delete_top_tracks(top_track_id):
    top_tracks = load_top_tracks(top_track_id)
    if top_tracks is not None:
        db.session.delete(top_tracks)
        db.session.commit()
        return True
    return False


# -------- Audio Features --------
def load_audio_feature(audio_feature_id):
    return AudioFeatures.query.filter_by(id=audio_feature_id).first()


def check_if_audio_feature_exists(audio_feature_id):
    if load_audio_feature(audio_feature_id) is not None:
        return True
    return False


def create_audio_features_object(audio_features: dict):
    track = load_track_object(audio_features['id'])
    if track is not None:
        if not check_if_audio_feature_exists(audio_features['id']):
            audio_features_object = AudioFeatures(track, **audio_features)
            db.session.add(audio_features_object)
            db.session.commit()
        return True
    return False
