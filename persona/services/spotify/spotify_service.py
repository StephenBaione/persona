import oauth2
import webbrowser
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
    def __init__(self):
        self.api_key = "3656a63cf4f547fd9c03f80a208c2e31"
        self.api_secret_key = "dbcfa2b2a2a242d0b675417adceb6c57"
        self.spotify_redirect_url = "http://127.0.0.1:5000/spotify/auth/redirect"
        self.oauth = OAuth2Session(self.api_key, redirect_uri=self.spotify_redirect_url, scope=AUTHORIZATION_SCOPE)

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

    def refresh_token(self, token):
        # Have to do this manually due to some weird OAuth2Session Error. Prevents from having to downgrade
        import base64
        import requests
        base_64_encoded_creds = base64.b64encode(f"{self.api_key}:{self.api_secret_key}")
        base_64_encoded_creds = base_64_encoded_creds.decode("ascii")
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": token["refresh_token"]
        }
        header = {"Authorization": f"Basic {base_64_encoded_creds}"}
        resp = requests.post("https://accounts.spotify.com/api/token", headers=header, data=payload)
        if resp.status_code != 200:
            print("Error obtaining refresh token")
            return None
        refresh_token = resp.json()
        return refresh_token


class SpotifyAPI:
    def __init__(self, oauth_token):
        self.api_key = "3656a63cf4f547fd9c03f80a208c2e31"
        self.api_secret_key = "dbcfa2b2a2a242d0b675417adceb6c57"
        self.client = OAuth2Session(self.api_key, token=oauth_token)

    def handle_error(self, e, func, *args, **kwargs):
        if isinstance(e, TokenExpiredError):
            refresh_token = SpotifyAuthentication.refresh_token(self.client.token)
            if refresh_token is None:
                raise TokenExpiredError("Could not refresh expired token")
            self.client.token = refresh_token
            func(*args, **kwargs)

    def get_current_user_profile(self):
        get_user_url = "https://api.spotify.com/v1/me"
        resp = self.client.get(get_user_url)
        if resp.status_code != 200:
            return "Error getting content. Check token expiration."
        data = resp.json()
        return data

    def get_users_top_artists(self, **kwargs):
        get_top_url = "https://api.spotify.com/v1/me/top/artists"
        type = "artists"
        time_range = kwargs.get("time_range", "short_term")
        limit = kwargs.get("limit", 10)
        offset = kwargs.get("offset", 0)
        get_top_url = f"{get_top_url}/?time_range={time_range}&limit={limit}&offset={offset}"
        resp = self.client.get(get_top_url)
        if resp.status_code != 200:
            print(resp.reason)
            return "Error getting top Artists"
        data = resp.json()
        return data
