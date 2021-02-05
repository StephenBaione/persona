import requests
import json
import os
import webbrowser

PATH_TO_CONFIG = os.path.join(os.environ["PWD"], "config.json")


def make_authorize_request(service):
    with open(PATH_TO_CONFIG, "r") as file:
        service_data = json.load(file)
    service_data = service_data['services'][service]
    credentials = service_data['credentials']
    urls = service_data['urls']['authorize']

    method = urls['method']
    url = urls['url']
    query_params = urls['query_params']
    body = urls['body']
    header = urls['header']

    if method == "GET":
        params = {}
        if query_params is not None:
            for key, value in query_params.items():
                params[key] = value
        req = requests.get(url, params=params)
        if req.status_code == 200 and req.reason == "OK":
            return req


def make_token_request(service, optional_parameters: dict):
    with open(PATH_TO_CONFIG, "r") as file:
        service_data = json.load(file)
    service_data = service_data['services'][service]
    credentials = service_data['credentials']
    urls = service_data['urls']['token_request']

    method = urls["method"]
    url = urls['url']
    query_params = urls['query_params']
    body = urls['body']
    header = urls['header']
    if method == "POST":
        post_body = {}
        for key, value in body.items():
            if value is None:
                if key in optional_parameters.keys() and optional_parameters[key] is not None:
                    post_body[key] = optional_parameters[key]
            else:
                post_body[key] = value
        req = requests.post(url, data=post_body, headers=header)
        return req
