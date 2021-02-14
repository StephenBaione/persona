from . import db


class Spotify(db.Model):
    __tablename__ = 'spotify'

    # ---- User Information ----
    id = db.Column(db.Integer, primary_key=True)
    display_name = db.Column(db.String(80))
    country = db.Column(db.String(20))
    email = db.Column(db.String(40), nullable=True)
    # Link to web API endpoint for user
    href = db.Column(db.String(80))
    # user's subscription level
    product = db.Column(db.String(15))
    # Spotify uri for user
    uri = db.Column(db.String(80))
    # Number of followers
    followers = db.Column(db.Integer())
    type = db.Column(db.String(20))

    # Explicit content settings
    filter_enabled = db.Column(db.Boolean(), default=False)
    filter_locked = db.Column(db.Boolean(), default=False)

    # External Url
    external_urls = db.Column(db.String(200))

    # ---- Relationships ----
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', uselist=False, back_populates='spotify')
    images = db.relationship("Image")

    # ---- Token Object ----
    access_token = db.Column(db.String(80))
    token_type = db.Column(db.String(20))
    expires_at = db.Column(db.Integer())
    refresh_token = db.Column(db.String(80))
    scopes = db.Column(db.String(80))

    def __init__(self, **kwargs):
        self.display_name = kwargs.get('display_name')
        self.country = kwargs.get('country')
        self.email = kwargs.get('email', None)
        self.href = kwargs.get('href')
        product = kwargs.get('product')
        if product == "open":
            product = "free"
        self.product = product
        self.uri = kwargs.get('uri')
        self.followers = kwargs.get('followers')
        self.filter_enabled = kwargs.get('filter_enabled')
        self.filter_locked = kwargs.get('filter_locked')
        self.external_url = kwargs.get('external_url')
        self.user = kwargs.get('user')
        # Assuming each image is passed in as dictionary object
        images = kwargs.get('images')
        if images is not None:
            for image in images:
                url = image['url']
                height = image.get('height', None)
                width = image.get('width', None)
                image_object = Image(url=url, height=height, width=width)
                self.images.append(image_object)
        token = kwargs.get("token")
        if token is not None:
            self.access_token = token.get('access_token')
            self.token_type = token.get('token_type')
            self.expires_at = token.get('expires_at')
            self.refresh_token = token.get('refresh_token')
            self.scopes = token.get('scopes')
        else:
            self.access_token = None
            self.token_type = None
            self.expires_at = None
            self.refresh_token = None
            self.scopes = None


class Image(db.Model):
    __tablename__ = "spotify_image"
    url = db.Column(db.String(80), primary_key=True)
    height = db.Column(db.Integer(), nullable=True)
    width = db.Column(db.Integer(), nullable=True)
    relationship = db.Column(db.Integer(), db.ForeignKey('spotify.id'))



