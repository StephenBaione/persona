from flask import Blueprint, request, session, redirect, url_for, render_template, flash, make_response
from persona.services.spotify.spotify_service import SpotifyAuthentication
from persona.services.twitter.twitter_service import TwitterAuthentication
from persona import db
from persona.model_handlers.persona_model_handler import verify_login, create_object_from_json, check_if_exists, load_user
from persona.forms import LoginForm
bp = Blueprint('auth', __name__, url_prefix="")


@bp.route('/login', methods=["POST", "GET"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        print(request.cookies.lists())
        if verify_login(username, password):
            session["logged_in"] = True
            session["username"] = username
            res = make_response(redirect(url_for("persona.home")))
            user = load_user('username', username)
            session["id"] = user.id
            res.set_cookie('test', 'test', max_age=60*60*24*30)
            # return redirect(url_for("persona.home"))
            return res
        else:
            flash("Invalid Credentials. Please try entering again.")
    return render_template("login.html", form=form)


@bp.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        if check_if_exists(username, email):
            flash("Username already exists or email already in use")
        else:
            create_object_from_json({"username": username, "email": email, "password": password})
            return redirect(url_for("auth.login"))
    return render_template("signup.html")



