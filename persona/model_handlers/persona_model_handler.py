from . import db, User
import time


def check_for_existing_persona_account(username):
    user = load_user('username', username)
    if user is None:
        return False
    return True


def update_user_object_from_json(user_id, data: dict):
    user = load_user('id', user_id)
    try:
        for field, value in data.items():
            user.__setattr__(field, value)
        db.session.commit()
        return True
    except Exception as e:
        print("Could not perform user update...")
        print(e)
        return False


def create_user_object_from_json(data: dict):
    try:
        username = data["username"]
        password = data["password"]
        email = data["email"]
        new_user = User(username=username, email=email, created_at=time.time_ns())
        new_user.password = password
        db.session.add(new_user)
        db.session.commit()
        return True
    except Exception as e:
        print("Could not create new user...")
        print(e)


def delete_user_object(user_id):
    user = load_user('id', user_id)
    if user is not None:
        db.session.delete(user)
        db.session.commit()
        return True
    return False


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
