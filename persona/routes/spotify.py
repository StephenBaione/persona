from flask import Blueprint, request, session, redirect, url_for, render_template
from persona.services.spotify.spotify_service import SpotifyAuthentication, SpotifyAPI
from persona.services.spotify.spotify_insights import top_track_audio_features_average
from persona.model_handlers import spotify_model_handler
from . import check_if_logged_in


bp = Blueprint('spotify', __name__, url_prefix="/spotify")


@bp.route('/', methods=["GET"])
def spotify_home():
    if not check_if_logged_in():
        return redirect(url_for("auth.login"))
    # Check if authorization has already occured
    user_id = session["id"]
    if not spotify_model_handler.check_for_existing_spotify_auth(user_id):
        return redirect(url_for("spotify.request_authorization"))
    token = spotify_model_handler.load_auth_token(user_id)
    sp = SpotifyAPI(token)
    print("Checking for valid token...")
    sp.check_and_handle_token_expiration()
    spotify = spotify_model_handler.load_object_from_user_id(session["id"])
    top_artists = sp.get_users_top_artists()
    top_tracks = sp.get_top_tracks()
    audio_features = sp.get_track_analysis(top_tracks)
    while audio_features is None:
        audio_features = sp.get_track_analysis(top_tracks)
    average_features = top_track_audio_features_average(audio_features)
    return render_template("spotify.html", spotify=spotify,
                           top_artists=top_artists,
                           top_tracks=top_tracks,
                           audio_features=audio_features,
                           average_top_features=average_features)


@bp.route('/auth/', methods=["GET"])
def request_authorization():
    if not check_if_logged_in():
        return redirect(url_for("auth.login"))
    authentication = SpotifyAuthentication()
    authentication.request_authorization()
    return "Performing Authentication"


@bp.route('/auth/redirect', methods=["GET"])
def request_token():
    if not check_if_logged_in():
        return redirect(url_for("auth.login"))
    code = request.args.get("code")
    authentication = SpotifyAuthentication()
    token = authentication.request_token(code)
    sp = SpotifyAPI(token)
    profile_data = sp.get_current_user_profile()
    profile_data["token"] = token
    user_id = session["id"]
    spotify_model_handler.create_spotify_object_from_json(user_id, profile_data)
    return redirect(url_for("spotify.spotify_home"))
