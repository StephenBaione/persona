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
        return refresh_token

    # -------- Token Methods --------
    def get_token(self):
        return self.oauth.token

    def set_token(self, token):
        self.oauth.token = token

    def check_for_token_expiration(self):
        token = self.oauth.token
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
        resp = self.client.get_url(get_user_url)
        if resp.status_code != 200:
            if self.check_and_handle_token_expiration():
                resp = self.client.get_url(get_user_url)
                data = resp.json()
                return data
        data = resp.json()
        return data

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
        resp = self.client.get_url(get_top_url, params)
        if resp.status_code != 200:
            print(resp.reason)
            return "Error getting top Artists"
        data = resp.json()
        return data["items"]

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
        resp = self.client.get_url(get_top_url, params)
        if resp.status_code != 200:
            print(resp.reason)
            return "Error getting top Artists"
        data = resp.json()
        return data["items"]

    def get_track_analysis(self, tracks):
        get_analysis_url = "https://api.spotify.com/v1/audio-features"
        track_ids = []
        for track in tracks:
            track_ids.append(track["id"])
        track_ids = ','.join(track_ids)
        params = {
            "ids": track_ids
        }
        resp = self.client.get_url(get_analysis_url, params)
        if resp.status_code != 200:
            print(resp.reason)
            return None
        data = resp.json()
        return data["audio_features"]

    def get_saved_tracks(self, **kwargs):
        get_tracks_url = "https://api.spotify.com/v1/me/tracks"
        market = kwargs.get("market", "US")
        limit = kwargs.get("limit", 50)
        offset = kwargs.get("offset", 0)
        params = {
            "market": market,
            "limit": limit,
            "offset": offset
        }
        resp = self.client.get_url(get_tracks_url, params)
        if resp.status_code != 200:
            print(resp.reason)
            return None
        data = resp.json()
        return data
