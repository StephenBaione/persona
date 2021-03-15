# TODO:// Create model_handler
from . import db
import datetime
from werkzeug.security import generate_password_hash, check_password_hash


FOLLOWERS_TABLE = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('friends', db.Boolean, default=False))


class User(db.Model):
    __tablename__ = 'user'

    # -------- User Information --------
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.Integer)
    followed = db.relationship(
        'User', secondary=FOLLOWERS_TABLE,
        primaryjoin=(FOLLOWERS_TABLE.c.followed_id == id),
        secondaryjoin=(FOLLOWERS_TABLE.c.follower_id == id),
        backref=db.backref('FOLLOWERS_TABLE', lazy='dynamic'), lazy='dynamic')

    # -------- Services --------
    twitter_connected = db.Column(db.Boolean(), unique=False, default=False)
    spotify_connected = db.Column(db.Boolean(), unique=False, default=False)
    spotify = db.relationship("Spotify", uselist=False, back_populates="user")
    twitter = db.relationship("Twitter", uselist=False, back_populates="user")


    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
