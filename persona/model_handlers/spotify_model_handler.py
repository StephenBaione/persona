from . import db
from . import User, Spotify
from . import persona_model_handler


def create_or_update_spotify_object_from_json(data: dict):
    display_name = data["display_name"]
    sp = Spotify.query.filter_by(display_name=display_name).first()
    if sp is not None:
        update_spotify_object_from_json(sp, data)
    else:
        create_spotify_object_from_json(sp, data)


def update_spotify_object_from_json(sp_object, data: dict):
    pass


def create_spotify_object_from_json(sp_object, data: dict):
    persona_username = data['username']
    #if not check_if_in_table('user', persona_username):
    #    raise ValueError(f"User: {persona_username} is not in database. "
    #                     f"Persona User must be created before service objects")
    persona_user = persona_model_handler.load_user("username", persona_username)
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
    access_token = token["access_token"]
    token_type = token["token_type"]
    expires_at = token["expires_at"]
    refresh_token = token["refresh_token"]
    scopes = token["scope"]

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
        "user": persona_user
    }
    spotify = Spotify(**kwargs)
    try:
        db.session.add(spotify)
        persona_user.spotify_connected = True
        db.session.commit()
    except Exception as e:
        print("Error adding spotify object to database\n")
        print(e)


def check_if_in_table(table_name, query_value):
    if table_name == "spotify":
        results = db.session.query(db.metadata.tables['spotify']).filter_by(display_name=query_value).all()
        if len(results) > 0:
            return True
    return False


def load_object_from_user_id(user_id):
    return Spotify.query.filter_by(user_id=user_id).first()
