from persona.model_handlers import spotify_model_handler
from persona.model_handlers import persona_model_handler
from persona.services.spotify.spotify_service import SpotifyAPI


class SpotifyServiceMiddleWare:
    def __init__(self, user_id):
        self.user = persona_model_handler.load_user('id', user_id)
        self.spotify = spotify_model_handler.load_object_from_user_id(user_id)
        token = spotify_model_handler.load_auth_token(user_id)
        self.spotify_service = SpotifyAPI(token)

    def get_and_save_top_tracks(self):
        top_tracks = self.spotify_service.get_top_tracks()
        spotify_model_handler.create_top_tracks(self.spotify, top_tracks)

    def get_and_save_top_artists(self):
        top_artists = self.spotify_service.get_users_top_artists()
        spotify_model_handler.create_top_artists(self.spotify, top_artists)

    def get_all_saved_tracks(self):
        offset = 0
        flag = True
        while flag:
            params = {
                "offset": offset,
                "limit": 50
            }
            tracks = self.spotify_service.get_saved_tracks(params)
            if len(tracks) < 50:
                flag = False
            spotify_model_handler.create_track_object_batch(tracks)
            offset += 49
