import oauth2
import webbrowser
import time
import json
from urllib import parse
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2.rfc6749.errors import TokenExpiredError

AUTHORIZATION_SCOPE = [
    # Images
    "ugc-image-upload",
    # Listening History
    "user-read-recently-played",
    "user-top-read",
    "user-read-playback-position",
    # Spotify Connect
    "user-read-playback-state",
    "user-modify-playback-state",
    "user-read-currently-playing",
    # Playback
    "app-remote-control",
    "streaming",
    # Playlists
    "playlist-modify-public",
    "playlist-modify-private",
    "playlist-read-private",
    "playlist-read-collaborative",
    # Follow
    "user-follow-modify",
    "user-follow-read",
    # Library
    "user-library-modify",
    "user-library-read",
    # Users
    "user-read-email",
    "user-read-private"]


class SpotifyAuthentication:
    def __init__(self, oauth_token=None):
        self.api_key = "3656a63cf4f547fd9c03f80a208c2e31"
        self.api_secret_key = "dbcfa2b2a2a242d0b675417adceb6c57"
        self.spotify_redirect_url = "http://127.0.0.1:5000/spotify/auth/redirect"
        if oauth_token is None:
            self.oauth = OAuth2Session(self.api_key, redirect_uri=self.spotify_redirect_url, scope=AUTHORIZATION_SCOPE)
        else:
            self.oauth = OAuth2Session(self.api_key, token=oauth_token)
        self.token = oauth_token

    # -------- Authentication Flow --------
    def request_authorization(self):
        spotify_auth_url = "https://accounts.spotify.com/authorize"
        client_id = self.api_key
        oauth = OAuth2Session(client_id, redirect_uri=self.spotify_redirect_url, scope=AUTHORIZATION_SCOPE)
        authorization_url, state = oauth.authorization_url(spotify_auth_url)
        webbrowser.open(authorization_url)

    def request_token(self, code):
        # spotify_redirect_uri = self.spotify_redirect_uri
        # Have to declare redirect uri as https so that OAuth2Session allows token request
        spotify_redirect_uri = "https://127.0.0.1:5000/spotify/auth/redirect"
        authorization_response = spotify_redirect_uri + "?code=" + code
        token = self.oauth.fetch_token("https://accounts.spotify.com/api/token",
                                       authorization_response=authorization_response,
                                       client_secret=self.api_secret_key)
        return token

    def execute_token_refresh(self, token):
        # Have to do this manually due to some weird OAuth2Session Error. Prevents from having to downgrade
        print("Refreshing Spotify Token")
        import base64
        import requests
        base_64_encoded_creds = base64.b64encode(bytes(f"{self.api_key}:{self.api_secret_key}", "ascii"))
        base_64_encoded_creds = base_64_encoded_creds.decode("ascii")
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": token["refresh_token"]
        }
        header = {"Authorization": f"Basic {base_64_encoded_creds}"}
        resp = requests.post("https://accounts.spotify.com/api/token", headers=header, data=payload)
        if resp.status_code != 200:
            print("Error obtaining refresh token")
            return False
        refresh_token = resp.json()
        # need to add expires_at field to refresh_token
        expires_at = time.time() + refresh_token["expires_in"]
        refresh_token['expires_at'] = expires_at
        return refresh_token

    # -------- Token Methods --------
    def get_token(self):
        return self.token

    def set_token(self, token):
        self.oauth.token = token
        self.token = token

    def check_for_token_expiration(self):
        token = self.token
        expires_at = token["expires_at"]
        if time.time() >= expires_at:
            return True
        return False

    # Request Response Methods
    def get_url(self, url, query_params: dict = None):
        client = self.oauth
        if query_params is None:
            return client.get(url)
        formatted_params = self.format_query_params(query_params)
        return client.get(f"{url}/?{formatted_params}")

    def format_query_params(self, params: dict):
        return "&".join([str(key) + "=" + str(val) for key, val in params.items()])


class SpotifyAPI:
    def __init__(self, oauth_token):
        self.api_key = "3656a63cf4f547fd9c03f80a208c2e31"
        self.api_secret_key = "dbcfa2b2a2a242d0b675417adceb6c57"
        self.client = SpotifyAuthentication(oauth_token=oauth_token)

    def check_and_handle_token_expiration(self):
        expired = self.check_for_token_expiration()
        if expired:
            print("Spotify token is expired.\nPerforming Token refresh...")
            new_token = self.client.execute_token_refresh(self.client.get_token())
            self.client.set_token(new_token)
            return True
        else:
            print("Token is not expired...")
            return False

    def check_for_token_expiration(self):
        return self.client.check_for_token_expiration()

    def get_current_user_profile(self):
        get_user_url = "https://api.spotify.com/v1/me"
        return self.get_api_endpoint(get_user_url)

    def get_users_top_artists(self, **kwargs):
        get_top_url = "https://api.spotify.com/v1/me/top/artists"
        time_range = kwargs.get("time_range", "short_term")
        limit = kwargs.get("limit", 10)
        offset = kwargs.get("offset", 0)
        params = {
            "time_range": time_range,
            "limit": limit,
            "offset": offset,
        }
        return self.get_api_endpoint(get_top_url, params)['items']

    # -------- Albums --------
    def get_albums(self, album_ids):
        get_album_url = "https://api.spotify.com/v1/albums"
        params = {
            "ids": ','.join(album_ids)
        }
        return self.get_api_endpoint(get_album_url, params)

    def get_albums_tracks(self, album_id, **kwargs):
        get_albums_tracks_url = f"https://api.spotify.com/v1/albums/{album_id}/tracks"
        limit = kwargs.get("limit", 50)
        offset = kwargs.get("offset", 0)
        params = {
            "limit": limit,
            "offset": offset
        }
        return self.get_api_endpoint(get_albums_tracks_url, params)

    def get_users_saved_albums(self, **kwargs):
        get_saved_albums_url = "https://api.spotify.com/v1/me/albums"
        params = {
            'limit': kwargs.get('limit', 50),
            'offset': kwargs.get('offset', 0),
        }
        return self.get_api_endpoint(get_saved_albums_url, params)

    # -------- Artists --------
    def get_artists(self, artist_ids):
        get_artists_url = "https://api.spotify.com/v1/artists"
        params = {
            "ids": ','.join(artist_ids)
        }
        return self.get_api_endpoint(get_artists_url, params)

    def get_artist_top_tracks(self, artist_id):
        get_artist_top_tracks_url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"
        return self.get_api_endpoint(get_artist_top_tracks_url)

    def get_artists_related_artists(self, artist_id):
        get_related_artists_url = f"https://api.spotify.com/v1/artists/{artist_id}/related-artists"
        return self.get_api_endpoint(get_related_artists_url)

    def get_artists_albums(self, artist_id, **kwargs):
        get_artist_albums_url = f"https://api.spotify.com/v1/artists/{artist_id}/albums"
        included_groups = kwargs.get("included_groups", None)
        if included_groups is not None:
            included_groups = ','.join(included_groups)
        limit = kwargs.get("limit", 50)
        offset = kwargs.get('offset', 0)
        params = {
            'limit': limit,
            'offset': offset
        }
        if included_groups is not None:
            params['included_groups'] = included_groups
        return self.get_api_endpoint(get_artist_albums_url, params)

    def get_users_followed_artists(self, **kwargs):
        get_followed_artists_url = "https://api.spotify.com/v1/me/following"
        after = kwargs.get('after', None)
        limit = kwargs.get('limit', 50)
        params = {
            "type": "artist",
            'limit': limit
        }
        if after is not None:
            params['after'] = after
        return self.get_api_endpoint(get_followed_artists_url, params)

    # -------- Tracks --------
    def get_track_recommendations(self, data: dict):
        get_recommendations_url = 'https://api.spotify.com/v1/recommendations'
        params = {
            'limit': data.get('limit', 100),
            'seed_artists': data['seed_artists'],
            'seed_genres': data['seed_genres'],
            'seed_tracks': data['seed_tracks']
        }
        min_acousticness = data.get("min_acousticness", None)
        if min_acousticness is not None:
            params["min_acousticness"] = min_acousticness
        max_acousticness = data.get("max_acousticness", None)
        if max_acousticness is not None:
            params["max_acousticness"] = max_acousticness
        target_acousticness = data.get("target_acousticness", None)
        if target_acousticness is not None:
            params["target_acousticness"] = target_acousticness
        min_danceability = data.get("min_danceability", None)
        if min_danceability is not None:
            params["min_danceability"] = min_danceability
        max_danceability = data.get("max_danceability", None)
        if max_danceability is not None:
            params["max_danceability"] = max_danceability
        target_danceability = data.get("target_danceability", None)
        if target_danceability is not None:
            params["target_danceability"] = target_danceability
        min_duration_ms = data.get("min_duration_ms", None)
        if min_duration_ms is not None:
            params["min_duration_ms"] = min_duration_ms
        max_duration_ms = data.get("max_duration_ms", None)
        if max_duration_ms is not None:
            params["max_duration_ms"] = max_duration_ms
        target_duration_ms = data.get("target_duration_ms", None)
        if target_duration_ms is not None:
            params["target_duration_ms"] = target_duration_ms
        min_energy = data.get("min_energy", None)
        if min_energy is not None:
            params["min_energy"] = min_energy
        max_energy = data.get("max_energy", None)
        if max_energy is not None:
            params["max_energy"] = max_energy
        target_energy = data.get("target_energy", None)
        if target_energy is not None:
            params["target_energy"] = target_energy
        min_instrumentalness = data.get("min_instrumentalness", None)
        if min_instrumentalness is not None:
            params["min_instrumentalness"] = min_instrumentalness
        max_instrumentalness = data.get("max_instrumentalness", None)
        if max_instrumentalness is not None:
            params["max_instrumentalness"] = max_instrumentalness
        target_instrumentalness = data.get("target_instrumentalness", None)
        if target_instrumentalness is not None:
            params["target_instrumentalness"] = target_instrumentalness
        min_key = data.get("min_key", None)
        if min_key is not None:
            params["min_key"] = min_key
        max_key = data.get("max_key", None)
        if max_key is not None:
            params["max_key"] = max_key
        target_key = data.get("target_key", None)
        if target_key is not None:
            params["target_key"] = target_key
        min_liveness = data.get("min_liveness", None)
        if min_liveness is not None:
            params["min_liveness"] = min_liveness
        max_liveness = data.get("max_liveness", None)
        if max_liveness is not None:
            params["max_liveness"] = max_liveness
        target_liveness = data.get("target_liveness", None)
        if target_liveness is not None:
            params["target_liveness"] = target_liveness
        min_loudness = data.get("min_loudness", None)
        if min_loudness is not None:
            params["min_loudness"] = min_loudness
        max_loudness = data.get("max_loudness", None)
        if max_loudness is not None:
            params["max_loudness"] = max_loudness
        target_loudness = data.get("target_loudness", None)
        if target_loudness is not None:
            params["target_loudness"] = target_loudness
        min_mode = data.get("min_mode", None)
        if min_mode is not None:
            params["min_mode"] = min_mode
        max_mode = data.get("max_mode", None)
        if max_mode is not None:
            params["max_mode"] = max_mode
        target_mode = data.get("target_mode", None)
        if target_mode is not None:
            params["target_mode"] = target_mode
        min_popularity = data.get("min_popularity", None)
        if min_popularity is not None:
            params["min_popularity"] = min_popularity
        max_popularity = data.get("max_popularity", None)
        if max_popularity is not None:
            params["max_popularity"] = max_popularity
        target_popularity = data.get("target_popularity", None)
        if target_popularity is not None:
            params["target_popularity"] = target_popularity
        min_speechiness = data.get("min_speechiness", None)
        if min_speechiness is not None:
            params["min_speechiness"] = min_speechiness
        max_speechiness = data.get("max_speechiness", None)
        if max_speechiness is not None:
            params["max_speechiness"] = max_speechiness
        target_speechiness = data.get("target_speechiness", None)
        if target_speechiness is not None:
            params["target_speechiness"] = target_speechiness
        min_tempo = data.get("min_tempo", None)
        if min_tempo is not None:
            params["min_tempo"] = min_tempo
        max_tempo = data.get("max_tempo", None)
        if max_tempo is not None:
            params["max_tempo"] = max_tempo
        target_tempo = data.get("target_tempo", None)
        if target_tempo is not None:
            params["target_tempo"] = target_tempo
        min_time_signature = data.get("min_time_signature", None)
        if min_time_signature is not None:
            params["min_time_signature"] = min_time_signature
        max_time_signature = data.get("max_time_signature", None)
        if max_time_signature is not None:
            params["max_time_signature"] = max_time_signature
        target_time_signature = data.get("target_time_signature", None)
        if target_time_signature is not None:
            params["target_time_signature"] = target_time_signature
        min_valence = data.get("min_valence", None)
        if min_valence is not None:
            params["min_valence"] = min_valence
        max_valence = data.get("max_valence", None)
        if max_valence is not None:
            params["max_valence"] = max_valence
        target_valence = data.get("target_valence", None)
        if target_valence is not None:
            params["target_valence"] = target_valence
        return self.get_api_endpoint(get_recommendations_url, params)

    def get_top_tracks(self, **kwargs):
        get_top_url = "https://api.spotify.com/v1/me/top/tracks"
        time_range = kwargs.get("time_range", "short_term")
        limit = kwargs.get("limit", 10)
        offset = kwargs.get("offset", 0)
        params = {
            "time_range": time_range,
            "limit": limit,
            "offset": offset,
        }
        return self.get_api_endpoint(get_top_url, params)['items']

    def get_tracks(self, track_ids):
        get_tracks_url = 'https://api.spotify.com/v1/tracks'
        params = {
            'ids': ','.join(track_ids)
        }
        return self.get_api_endpoint(get_tracks_url, params)

    def get_track_analysis(self, tracks):
        get_analysis_url = "https://api.spotify.com/v1/audio-features"
        track_ids = []
        for track in tracks:
            track_ids.append(track["id"])
        track_ids = ','.join(track_ids)
        params = {
            "ids": track_ids
        }
        results = self.get_api_endpoint(get_analysis_url, params)
        return results['audio_features'] if results is not None else None

    def get_saved_tracks(self, params=None):
        get_tracks_url = "https://api.spotify.com/v1/me/tracks"
        return self.get_api_endpoint(get_tracks_url, params)["items"]

    def get_recently_played_tracks(self, **kwargs):
        get_recently_played_url = 'https://api.spotify.com/v1/me/player/recently-played'
        params = {
            'limit': kwargs.get('limit', 50)
        }
        after = kwargs.get('after', None)
        if after is not None:
            params['after'] = after
        else:
            before = kwargs.get('before', None)
            if before is not None:
                params['before'] = before
        return self.get_api_endpoint(get_recently_played_url, params)

    def search_for_item(self, query_param, type, **kwargs):
        get_search_url = 'https://api.spotify.com/v1/search'
        limit = kwargs.get('limit', 50)
        offset = kwargs.get('offset', 0)
        params = {
            "q": query_param,
            "type": type,
            'limit': limit,
            'offset': offset
        }

        include_external = kwargs.get('include_external', None)
        if include_external is not None:
            params['include_external'] = include_external
        return self.get_api_endpoint(get_search_url, params)

    def get_api_endpoint(self, base_url, params=None):
        self.check_and_handle_token_expiration()
        if params is None:
            resp = self.client.get_url(base_url)
        else:
            resp = self.client.get_url(base_url, params)
        if resp.status_code != 200:
            if resp.status_code == 429:
                time.sleep(5)
            print(resp.text)
            return None
        data = resp.json()
        return data
