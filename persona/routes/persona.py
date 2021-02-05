from flask import Blueprint, session, redirect, url_for, render_template
from persona.model_handlers import persona_model_handler, spotify_model_handler
from persona.services.spotify.spotify_service import SpotifyAPI

bp = Blueprint("persona", __name__, "")


@bp.route('/')
@bp.route('/home')
def home():
    try:
        logged_in = session["logged_in"]
        username = session["username"]
        if logged_in:
            user = persona_model_handler.load_user("username", username)
            spotify = None
            if user.spotify_connected:
                spotify = spotify_model_handler.load_object_from_user_id(user.id)

            return render_template("home.html", user=user, spotify=spotify)
        else:
            return redirect(url_for("auth.login"))
    except Exception as e:
        return redirect(url_for("auth.login"))
