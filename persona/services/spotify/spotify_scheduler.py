from apscheduler.schedulers.background import BackgroundScheduler
from .spotify_service import SpotifyAPI
from persona.model_handlers import spotify_model_handler


class SpotifyScheduler(BackgroundScheduler):
    def __init__(self, user_id):
        super(SpotifyScheduler, self).__init__()
        self.user_id = user_id
        token = spotify_model_handler.load_auth_token(user_id)
        self.spotify = SpotifyAPI(token)

        self.add_job(self.spotify.get_top_tracks, 'interval', days=1)
        self.add_job(self.spotify.get_users_top_artists, 'interval', days=1)
