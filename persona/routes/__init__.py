from flask import session


def check_if_logged_in():
    try:
        logged_in = session["logged_in"]
        username = session["username"]
        if logged_in and (username is not None):
            return True
    except Exception as e:
        return False


