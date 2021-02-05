# TODO:// Create model_handler
from . import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    twitter_connected = db.Column(db.Boolean(), unique=False, default=False)
    spotify_connected = db.Column(db.Boolean(), unique=False, default=False)
    spotify = db.relationship("Spotify", uselist=False, back_populates="user")

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
