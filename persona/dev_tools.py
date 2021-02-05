from . import db

from .models.persona_models import User
from .models.spotify_models import Spotify
from .model_handlers import spotify_model_handler


def reset_database():
    db.drop_all()
    db.create_all()


def get_db_tables():
    return db.engine.table_names()


def initialize_database_test():
    new_user_1 = User(username="stephenbaione", email="sbaione@email.sc.edu")
    new_user_1.password = "Huskies870920!@"

    new_user_2 = User(username="fsociety", email="robot@robot.com")
    new_user_2.password = "mrrobot"



    db.session.add(new_user_1)
    db.session.add(new_user_2)

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

    db.session.commit()

