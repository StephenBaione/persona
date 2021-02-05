from flask import Blueprint, request, session, redirect, url_for, render_template
from persona.services.spotify.spotify_service import SpotifyAuthentication, SpotifyAPI
from persona.model_handlers import spotify_model_handler
from . import check_if_logged_in


bp = Blueprint('spotify', __name__, url_prefix="/spotify")


@bp.route('/', methods=["GET"])
def spotify_home():
    if not check_if_logged_in():
        return redirect(url_for("auth.login"))
    try:
        token = session['spotify_token']
    except Exception as e:
        return redirect(url_for("spotify.request_authorization"))
    sp = SpotifyAPI(token)
    profile_data = sp.get_current_user_profile()
    profile_data["username"] = session["username"]
    profile_data["token"] = token
    spotify_model_handler.create_or_update_spotify_object_from_json(profile_data)
    spotify = spotify_model_handler.load_object_from_user_id(session["id"])
    top_tracks = sp.get_users_top_artists()
    print(top_tracks)
    return render_template("spotify.html", spotify=spotify, top_tracks=top_tracks)


@bp.route('/auth/', methods=["GET"])
def request_authorization():
    if not check_if_logged_in():
        return redirect(url_for("auth.login"))
    authentication = SpotifyAuthentication()
    authentication.request_authorization()
    return "Performing Authentication"


@bp.route('/auth/redirect', methods=["GET"])
def request_token():
    code = request.args.get("code")
    authentication = SpotifyAuthentication()
    token = authentication.request_token(code)
    session["spotify_token"] = token
    return redirect(url_for("spotify.spotify_home"))
