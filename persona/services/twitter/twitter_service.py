import os
import sys

import oauth2
import webbrowser
import json
from urllib import parse
from requests_oauthlib import OAuth1Session


class TwitterAuthentication:
    def __init__(self):
        self.api_key = "dXQUrfBR8juh1iUyoMcgkiqqB"
        self.api_secret_key = "TQiZ8N9navBdcaSBmiJ9GSCVZNbgqaHwxRSU5wl7NdAMucQ4Mt"
        self.twitter_callback_url = "http://127.0.0.1:5000/auth/twitter/redirect/"

    def fetch_request_token(self):
        oauth = OAuth1Session(self.api_key, client_secret=self.api_secret_key)
        fetch_response = oauth.fetch_request_token("https://api.twitter.com/oauth/request_token")
        print(fetch_response)
        resource_owner_key = fetch_response["oauth_token"]
        resource_owner_secret = fetch_response["oauth_token_secret"]
        authorization_url = oauth.authorization_url("https://api.twitter.com/oauth/authorize")
        webbrowser.open(authorization_url)
        return resource_owner_key, resource_owner_secret

    def fetch_access_token(self, resource_owner_key, resource_owner_secret, oauth_verifier):
        oauth = OAuth1Session(self.api_key,
                              client_secret=self.api_secret_key,
                              resource_owner_key=resource_owner_key,
                              resource_owner_secret=resource_owner_secret,
                              verifier=oauth_verifier)
        oauth_token = oauth.fetch_access_token("https://api.twitter.com/oauth/access_token")
        return oauth_token


class TwitterAPI:
    def __init__(self, oauth_token, oauth_verifier, user_id):
        self.oauth_token = oauth_token
        self.oauth_verifier = oauth_verifier
        self.user_id = user_id
        print(user_id)
        self.token = oauth2.Token(oauth_token, oauth_verifier)
        self.api_key = "dXQUrfBR8juh1iUyoMcgkiqqB"
        self.api_secret_key = "TQiZ8N9navBdcaSBmiJ9GSCVZNbgqaHwxRSU5wl7NdAMucQ4Mt"
        consumer = oauth2.Consumer(self.api_key, self.api_secret_key)
        self.client = oauth2.Client(consumer, self.token)

    def show_user(self):
        resp, content = self.client.request(f"https://api.twitter.com/1.1/users/show.json?user_id={self.user_id}",
                                            "GET")
        data = json.loads(content.decode("utf-8"))
        print(data)



