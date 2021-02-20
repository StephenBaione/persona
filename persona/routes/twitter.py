from flask import Blueprint, request, session, redirect, url_for, render_template
from persona.services.twitter.twitter_service import TwitterAuthentication, TwitterAPI
from persona.services.twitter import twitter_insights
from persona.model_handlers import twitter_model_handler
from . import check_if_logged_in

bp = Blueprint('twitter', __name__, url_prefix="/twitter")


@bp.route("/", methods=["GET"])
def twitter_home():
    if not check_if_logged_in():
        return redirect(url_for("auth.login"))
    user_id = session["id"]
    if not twitter_model_handler.check_for_existing_twitter_auth(user_id):
        return redirect(url_for("twitter.request_authorization"))
    token = twitter_model_handler.load_auth_token(user_id)
    tw = TwitterAPI(token["oauth_token"], token["oauth_token_secret"], user_id)
    twitter = twitter_model_handler.load_object_from_user_id(user_id)
    user_tweets_params = {
        "user_id": twitter.id,
        "count": 200
    }
    user_tweets = tw.get_user_tweets(**user_tweets_params)
    tweet_creation_status, failing_tweets = twitter_model_handler.create_multiple_tweet_objects(user_tweets)
    if not tweet_creation_status:
        print(f"Total Failing Tweets: {len(failing_tweets)}")
    top_tweets = twitter_insights.calulate_owned_engagement(twitter.id)
    return render_template("twitter.html", top_tweets=top_tweets)


@bp.route('/auth/', methods=["GET", "POST"])
def request_authorization():
    twitter_authentication = TwitterAuthentication()
    resource_owner_key, resource_owner_secret = twitter_authentication.fetch_request_token()
    session["twitter_resource_owner_key"] = resource_owner_key
    session["twitter_resource_owner_secret"] = resource_owner_secret
    return "Initiating authentication request"


@bp.route('/auth/redirect', methods=["GET"])
def request_token():
    user_id = session["id"]
    twitter_authentication = TwitterAuthentication()
    oauth_token = request.args.get("oauth_token")
    oauth_token_secret = request.args.get("oauth_verifier")
    resource_owner_key = session["twitter_resource_owner_key"]
    resource_owner_secret = session["twitter_resource_owner_secret"]
    token = twitter_authentication.fetch_access_token(resource_owner_key, resource_owner_secret, oauth_token_secret)
    tw = TwitterAPI(token["oauth_token"], token["oauth_token_secret"], token["user_id"])
    profile_data = tw.show_user()
    print(profile_data)
    profile_data["token"] = token
    twitter_model_handler.create_twitter_object_from_json(user_id, profile_data)
    return redirect(url_for("twitter.twitter_home"))
