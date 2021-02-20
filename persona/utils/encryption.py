from cryptography.fernet import Fernet
import base64

from persona.model_handlers import persona_model_handler
from persona import User

# TODO:// Storing this here is asking to get hacked
KEY = b'o_tdvJVG9D0jn7Z3aTLI6gUvEpZWZmcvLfpQs6YZiiw='


def generate_login_token(user_id, username):
    f = Fernet(KEY)
    login_string = f"user_id:{user_id},username:{username}"
    login_string = base64.b64encode(login_string.encode())
    token = f.encrypt(login_string)
    return token


def check_login_token(token):
    f = Fernet(KEY)
    if type(token) != bytes:
        token = token.encode()
    decoded_token = base64.b64decode(f.decrypt(token)).decode('ascii')
    import re
    try:
        user_id, username = re.findall("^user_id:(\d+),username:(\w+)", decoded_token)[0]
        user = User.query.filter_by(id=user_id).filter_by(username=username).first()
        if user is not None:
            return True, user_id, username
    except Exception as e:
        return False, None, None
    return False, None, None





