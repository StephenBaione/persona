from .models import spotify_model_handler
from persona import dev_tools


# STATUS: WORKING
def test_spotify_model_handler():
    # Reset and Initialize database
    dev_tools.reset_database()
    dev_tools.initialize_database_test()

    # Define spotify objects
    data = {
        "username": "fsociety",
        "country": "US",
        "display_name": "fsociety_music",
        "email": "robot@robot.com",
        "explicit_content": {"filter_enabled": False, "filter_locked": False},
        "external_urls": {'spotify': 'url'},
        "followers": {"total": 500},
        "href": "href",
        "product": "free",
        "type": "user",
        "images": None,
        "uri": "uri"
    }

    exists = spotify_model_handler.check_if_in_table('spotify', 'fsociety_music')
    print(exists)
    if not exists:
        spotify_model_handler.create_spotify_object_from_json(data)

