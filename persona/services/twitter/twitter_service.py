import os
import sys

import oauth2
import webbrowser
import json
from urllib import parse
from requests_oauthlib import OAuth1Session


class TwitterAuthentication:
    def __init__(self, oauth_token=None, oauth_token_secret=None):
        """
        Perform Twitter authentication using OAuth1 flow and make authenticated requests
        :param oauth_token: Oauth Token obtained through OAuth1 flow
        :param oauth_token_secret: Oauth Token Secret obtained through OAuth1 flow
        """
        # Credentials used for Twitter Web API
        self.api_key = "dXQUrfBR8juh1iUyoMcgkiqqB"
        self.api_secret_key = "TQiZ8N9navBdcaSBmiJ9GSCVZNbgqaHwxRSU5wl7NdAMucQ4Mt"
        self.twitter_callback_url = "http://127.0.0.1:5000/auth/twitter/redirect/"

        # Create TwitterAuthentication for user which we have not obtained access token for
        if oauth_token is None or oauth_token_secret is None:
            self.oauth = OAuth1Session(self.api_key, client_secret=self.api_secret_key)
            self.token = None
        # Create TwtterAuthentication for user we have obtained access token for
        else:
            self.oauth = OAuth1Session(self.api_key,
                                       client_secret=self.api_secret_key,
                                       resource_owner_key=oauth_token,
                                       resource_owner_secret=oauth_token_secret)
            # Structure token for easy reference
            self.token = {
                "oauth_token": oauth_token,
                "oauth_token_secret": oauth_token_secret
            }

    def fetch_request_token(self):
        """
        First step in Twitter OAuth1 Authentication flow
        :return: credentials used to fetch access token
        """
        # request credentials
        oauth = self.oauth
        fetch_response = oauth.fetch_request_token("https://api.twitter.com/oauth/request_token")
        # abstract credentials and open authorization url
        resource_owner_key = fetch_response["oauth_token"]
        resource_owner_secret = fetch_response["oauth_token_secret"]
        authorization_url = oauth.authorization_url("https://api.twitter.com/oauth/authorize")
        # opening authorization url triggers explicit permission -> redirect
        webbrowser.open(authorization_url)
        return resource_owner_key, resource_owner_secret

    def fetch_access_token(self, resource_owner_key, resource_owner_secret, oauth_verifier):
        """
        Obtain access token to complete authentication process
        :param resource_owner_key: Obtained from fetch_request_token
        :param resource_owner_secret: Obtained from fetch_access_token
        :param oauth_verifier: Obtained from arg in redirect url
        :return:
        """
        # Create client to complete flow
        oauth = OAuth1Session(self.api_key,
                              client_secret=self.api_secret_key,
                              resource_owner_key=resource_owner_key,
                              resource_owner_secret=resource_owner_secret,
                              verifier=oauth_verifier)
        oauth_token = oauth.fetch_access_token("https://api.twitter.com/oauth/access_token")
        return oauth_token

    def get_token(self):
        return self.token

    def set_token(self, token):
        try:
            # Two fields required for valid token
            oauth_token = token["oauth_token"]
            oauth_token_secret = token["oauth_token_secret"]
            if oauth_token is not None and oauth_token_secret is not None:
                self.token = {
                    "oauth_token": oauth_token,
                    "oauth_token_secret": oauth_token_secret}
                # set variables for oauth
                # oauth resource_owner_key = persona oauth_token
                # oauth resource_owner_secret = persona oauth_token_secret
                self.oauth.__setattr__("resource_owner_key", oauth_token)
                self.oauth.__setattr__("resource_owner_secret", oauth_token_secret)
                return True
        except Exception as e:
            print(e)
        return False

    def get_url(self, url, query_params: dict = None):
        client = self.oauth
        if query_params is None:
            return client.get(url)
        formatted_params = self.format_query_params(params=query_params)
        return client.get(f"{url}?{formatted_params}")

    def format_query_params(self, params: dict):
        return "&".join([str(key) + "=" + str(val) for key, val in params.items()])


class TwitterAPI:
    # TODO:// Add more endpoints
    def __init__(self, oauth_token, oauth_token_secret, user_id):
        self.api_key = "dXQUrfBR8juh1iUyoMcgkiqqB"
        self.api_secret_key = "TQiZ8N9navBdcaSBmiJ9GSCVZNbgqaHwxRSU5wl7NdAMucQ4Mt"
        self.client = TwitterAuthentication(oauth_token=oauth_token, oauth_token_secret=oauth_token_secret)
        self.user_id = user_id

    def show_user(self):
        get_user_url = "https://api.twitter.com/1.1/users/show.json"
        params = {
            "user_id": self.user_id
        }
        resp = self.client.get_url(get_user_url, params)
        if resp.status_code != 200:
            print(resp.reason)
            print(resp.url)
            return None
        return resp.json()

    def get_user_tweets(self, **kwargs):
        get_user_tweets_url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
        params = kwargs
        resp = self.client.get_url(get_user_tweets_url, params)
        if resp.status_code != 200:
            print(resp.reason)
            print(resp.url)
            return None
        return resp.json()
