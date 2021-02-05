@bp.route('/twitter/', methods=["GET", "POST"])
def request_twitter_auth_access():
    twitter_authentication = TwitterAuthentication()
    resource_owner_key, resource_owner_secret = twitter_authentication.fetch_request_token()
    session["twitter_resource_owner_key"] = resource_owner_key
    session["twitter_resource_owner_secret"] = resource_owner_secret
    return "Initiating authentication request"


@bp.route('/twitter/redirect/', methods=["GET"])
def twitter_auth_redirect():
    twitter_authentication = TwitterAuthentication()
    oauth_token = request.args.get("oauth_token")
    oauth_verifier = request.args.get("oauth_verifier")
    resource_owner_key = session["twitter_resource_owner_key"]
    resource_owner_secret = session["twitter_resource_owner_secret"]
    token = twitter_authentication.fetch_access_token(resource_owner_key, resource_owner_secret, oauth_verifier)
    session["twitter_resource_owner_key"] = token["oauth_token"]
    session["twitter_resource_owner_secret"] = token["oauth_token_secret"]
    session["twitter_user_id"] = token["user_id"]
    session["twitter_screen_name"] = token["screen)_name"]
    return f"Oauth_token: {token}"