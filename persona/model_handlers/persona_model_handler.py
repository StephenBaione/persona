from . import db, User


def create_object_from_json(data: dict):
    username = data["username"]
    password = data["password"]
    email = data["email"]

    new_user = User(username=username, email=email)
    new_user.password = password

    db.session.add(new_user)
    db.session.commit()


def load_user(key, value):
    user = None
    if key == "username":
        user = User.query.filter_by(username=value).first()
    elif key == "id":
        user = User.query.filter_by(id=value).first()
    return user


def check_if_exists(username, email):
    results = User.query.filter_by(username=username).all()
    if len(results) > 0:
        user = results[0]
        if user.email == email:
            return True
    return False


def verify_login(username, password):
    results = User.query.filter_by(username=username).all()
    if len(results) > 0:
        user = results[0]
        if user.verify_password(password):
            return True
    return False
