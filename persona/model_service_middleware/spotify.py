from persona.model_handlers import spotify_model_handler
from persona.model_handlers import persona_model_handler
from persona.services.spotify.spotify_service import SpotifyAPI
from tqdm import tqdm


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
            tracks = [track['track'] for track in tracks]
            if len(tracks) < 50:
                flag = False
            track_objects = spotify_model_handler.create_track_object_batch(tracks, return_tracks=True)
            offset += 49
            spotify_model_handler.add_to_saved_tracks_batch(self.spotify, track_objects)

    def get_analysis_for_all_saved_tracks(self):
        saved_tracks = self.spotify.saved_tracks
        saved_track_id_dict = [{"id": track.id} for track in saved_tracks]
        results = []
        if len(saved_track_id_dict) > 100:
            offset = 0
            for i in tqdm(range(len(saved_track_id_dict) % 100 + 1)):
                saved_track_batch = saved_track_id_dict[offset: offset + 100]
                batch_results = self.spotify_service.get_track_analysis(saved_track_batch)
                for result in batch_results:
                    results.append(result)
                offset += 100
        else:
            results = self.spotify_service.get_track_analysis(saved_track_id_dict)
        spotify_model_handler.create_audio_features_object_batch(results)

    def track_listening_session(self):
        pass
