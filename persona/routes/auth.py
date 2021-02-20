from flask import Blueprint, request, session, redirect, url_for, render_template, flash, make_response
from persona.services.spotify.spotify_service import SpotifyAuthentication
from persona.services.twitter.twitter_service import TwitterAuthentication
from persona import db
from persona.model_handlers.persona_model_handler import verify_login, create_user_object_from_json, check_if_exists, load_user
from persona.forms import LoginForm
from persona.utils import encryption
bp = Blueprint('auth', __name__, url_prefix="")


@bp.route('/login', methods=["POST", "GET"])
def login():
    # Check if encrypted login token has already been set as cookie
    login_token = request.cookies.get("login", None)
    if login_token is not None:
        # Check if login token is valid
        valid, user_id, username = encryption.check_login_token(login_token)
        if valid:
            # Set needed session variables and complete login process
            session["logged_in"] = True
            session["username"] = username
            session["id"] = user_id
            return redirect(url_for("persona.home"))
    form = LoginForm(request.form)
    # If user has submitted login credentials
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        # Check if login credentials are valid
        if verify_login(username, password):
            # Load user and set necessary session variables
            user = load_user('username', username)
            session["logged_in"] = True
            session["username"] = username
            session["id"] = user.id
            # Create response, including login token as cookie
            res = make_response(redirect(url_for("persona.home")))
            res.set_cookie('login', encryption.generate_login_token(user.id, user.username), max_age=60*60*24*30)
            return res
        else:
            flash("Invalid Credentials. Please try entering again.")
    return render_template("login.html", form=form)


@bp.route("/signup", methods=["POST", "GET"])
def signup():
    # Signup has been submitted
    if request.method == "POST":
        # Obtain credentials from form
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        # Don't think this works. Styling for this page is getting done later
        if check_if_exists(username, email):
            flash("Username already exists or email already in use")
        else:
            # Create user in database
            create_user_object_from_json({"username": username, "email": email, "password": password})
            return redirect(url_for("auth.login"))
    return render_template("signup.html")



