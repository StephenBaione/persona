from persona.model_handlers import spotify_model_handler
from persona.services.spotify.spotify_service import SpotifyAPI


class SpotifyMiddleware:
    def __init__(self, user_id):
        # Load authorization token
        token = spotify_model_handler.load_auth_token(user_id)
        self.spotify_service = SpotifyAPI(token)

    def save_all_users_tracks(self, save_features=False):
        offset = 0
        params = {
            'limit': 50,
        }
        iterate = True
        while iterate:
            params['offset'] = offset
            saved_tracks = self.spotify_service.get_saved_tracks(params)
            if len(saved_tracks) != 50:
                iterate = False
            tracks = [track['track'] for track in saved_tracks]
            features = self.spotify_service.get_track_analysis(tracks)
            spotify_model_handler.create_track_object_batch(tracks)
            for feature in features:
                spotify_model_handler.create_audio_features_object(feature)
            offset += 49
            print(f"Saving track {offset + len(saved_tracks)}")

    def get_and_save_audio_features_object(self, track):
        all_tracks = spotify_model_handler.TrackObject.query.all()
        all_tracks = [track.toJson() for track in all_tracks]
        non_analyzed_tracks = [track for track in all_tracks if not spotify_model_handler.check_if_audio_feature_exists(track['id'])]
        for track in non_analyzed_tracks:
            features = self.spotify_service.get_track_analysis([track])
            if features is not None:
                features = features[0]
                spotify_model_handler.create_audio_features_object(features)

