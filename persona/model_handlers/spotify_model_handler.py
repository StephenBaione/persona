from . import db
from . import User, Spotify
from . import persona_model_handler


def check_for_existing_spotify_auth(user_id):
    spotify = Spotify.query.filter_by(id=user_id).first()
    if spotify is None:
        return False
    return True


def update_spotify_object_from_json(user_id, data: dict):
    sp_object = load_object_from_user_id(user_id)
    if sp_object is None:
        return False
    for field, value in data.items():
        sp_object.__setattr__(field, value)
    db.session.commit()
    return True


def create_spotify_object_from_json(user_id, data: dict):
    if check_for_existing_spotify_auth(user_id):
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
    except Exception as e:
        print("Error adding spotify object to database\n")
        print(e)


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


def check_if_in_table(table_name, query_value):
    if table_name == "spotify":
        results = db.session.query(db.metadata.tables['spotify']).filter_by(display_name=query_value).all()
        if len(results) > 0:
            return True
    return False


def load_object_from_user_id(user_id):
    return Spotify.query.filter_by(user_id=user_id).first()
