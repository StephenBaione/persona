from . import db


class Twitter(db.Model):
    __tablename__ = "twitter"

    # ---- User Information ----
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    screen_name = db.Column(db.String(80))
    location = db.Column(db.String(80), nullable=True, default="unknown")
    url = db.Column(db.String(80))
    description = db.Column(db.String(120))
    protected = db.Column(db.Boolean(), default=False)
    verified = db.Column(db.Boolean(), default=False)
    followers_count = db.Column(db.Integer)
    friends_count = db.Column(db.Integer)
    listed_count = db.Column(db.Integer)
    favourites_count = db.Column(db.Integer)
    statuses_count = db.Column(db.Integer)
    created_at = db.Column(db.String(40))
    profile_image_url = db.Column(db.String(80))

    # -------- Relationships --------
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', uselist=False, back_populates='twitter')

    # -------- Token Information --------
    oauth_token = db.Column(db.String(120))
    oauth_token_secret = db.Column(db.String(120))

    # -------- Tweets --------
    # One to Many relationship: Twitter -> Tweet
    tweets = db.relationship("Tweet", backref="twitter", lazy=True)

    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.screen_name = kwargs.get("screen_name")
        self.location = kwargs.get("location", None)
        self.url = kwargs.get("url")
        self.description = kwargs.get("description")
        self.protected = kwargs.get("protected")
        self.verified = kwargs.get("verified")
        self.followers_count = kwargs.get("followers_count")
        self.friends_count = kwargs.get("friends_count")
        self.listed_count = kwargs.get("listed_count")
        self.favourites_count = kwargs.get("favourites_count")
        self.statuses_count = kwargs.get("statuses_count")
        self.created_at = kwargs.get("created_at")
        self.profile_image_url = kwargs.get("profile_image_url")
        self.user = kwargs.get("user")

        # Parse token for field update
        token = kwargs.get("token")
        if token is not None:
            self.oauth_token = token["oauth_token"]
            self.oauth_token_secret = token["oauth_token_secret"]
        else:
            self.oauth_token = None
            self.oauth_token_secret = None


class Tweet(db.Model):
    __tablename__ = "tweet"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('twitter.id'), nullable=False)
    created_at = db.Column(db.String(80))
    text = db.Column(db.String(140))
    source = db.Column(db.String(50))
    truncated = db.Column(db.Boolean, default=False)
    in_reply_to_status_id = db.Column(db.Integer, nullable=True)
    in_reply_to_screen_name = db.Column(db.Integer, nullable=True)
    in_reply_to_user_id = db.Column(db.Integer, nullable=True)
    # TODO:// Create Coordinates object for one to one relationship
    coordinates_latitude = db.Column(db.Integer, nullable=True)
    coordinates_longitude = db.Column(db.Integer, nullable=True)
    # TODO:// Create Places object for one to one relationship
    is_quote_status = db.Column(db.Boolean, default=False)
    quote_status_id = db.Column(db.Integer, db.ForeignKey('tweet.id'), nullable=True)
    quoted_status = db.relationship("Tweet", foreign_keys=[quote_status_id])
    retweeted_status_id = db.Column(db.Integer, db.ForeignKey('tweet.id'), nullable=True)
    retweeted_status = db.relationship("Tweet", foreign_keys=[retweeted_status_id])
    quote_count = db.Column(db.Integer)
    reply_count = db.Column(db.Integer)
    retweet_count = db.Column(db.Integer)
    favorite_count = db.Column(db.Integer)
    # TODO:// Create Entities object for one to one relationship
    # TODO:// Create Extended Entities object for one to one relationship
    favorited = db.Column(db.Boolean, default=False, nullable=True)
    retweeted = db.Column(db.Boolean, default=False, nullable=True)
    possibly_sensitive = db.Column(db.Boolean, default=False, nullable=True)
    filter_level = db.Column(db.String(80))
    lang = db.Column(db.String(3), nullable=True)
    # TODO:// Figure out Array of Rules Objects

    def __init__(self, **kwargs):
        self.id = kwargs["id"]
        self.user_id = kwargs["user"]["id"]
        self.twitter_user = kwargs["user"]
        self.created_at = kwargs["created_at"]
        self.text = kwargs["text"]
        self.source = kwargs["source"]
        self.truncated = kwargs["truncated"]
        self.in_reply_to_status_id = kwargs.get("in_reply_to_status_id", None)
        self.in_reply_to_user_id = kwargs.get("in_reply_to_user_id", None)
        self.in_reply_to_screen_name = kwargs.get("in_reply_to_screen_name", None)
        coordinates = kwargs.get("coordinates", None)
        if coordinates is not None:
            self.coordinates_latitude = coordinates["coordinates"]["coordinates"][0]
            self.coordinates_longitude = coordinates["coordinates"]["coordinates"][1]
        self.is_quote_status = kwargs["is_quote_status"]
        self.quote_status_id = kwargs.get("quote_status_id", None)
        if self.quote_status_id is not None:
            self.quoted_status = kwargs["quoted_status"]
        self.retweeted_status_id = kwargs.get("retweeted_status_id", None)
        if self.retweeted_status_id is not None:
            self.retweeted_status = kwargs["retweeted_status"]
        self.quote_count = kwargs.get("quote_count", None)
        self.reply_count = kwargs.get("reply_count", None)
        self.retweet_count = kwargs.get("retweet_count")
        self.favorite_count = kwargs.get("favorite_count", None)
        self.favorited = kwargs.get("favorited", None)
        self.retweeted = kwargs.get("retweeted", None)
        self.possibly_sensitive = kwargs.get("possibly_sensitive", None)
        self.filter_level = kwargs.get("filter_level", None)
        self.lang = kwargs.get("lang", None)

