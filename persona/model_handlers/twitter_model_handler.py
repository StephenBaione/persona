from . import db
from . import User, Twitter, Tweet
from . import persona_model_handler


def check_for_existing_twitter_auth(user_id):
    """
    Check if Twitter Object exists in database
    :param user_id: id of User Object
    :return: Boolean - Whether Twitter object exists
    """
    twitter = Twitter.query.filter_by(user_id=user_id).first()
    if twitter is None:
        return False
    return True


def update_twitter_object_from_json(user_id, data: dict):
    """
    Update field values for existing Twitter object
    :param user_id: id of User Object
    :param data: Data that will be inserted into Twitter object's fields
                 (Reference Twitter Model for valid field names)
    :return: Boolean - Whether or not update was successful
    """
    tw_object = load_object_from_user_id(user_id)
    if tw_object is not None:
        for field, value in data.items():
            tw_object.__setattr__(field, value)
        db.session.commit()
        return True
    return False


def create_twitter_object_from_json(user_id, data: dict):
    """
    Create a Twitter Object from data dictionary
    :param user_id: id of User Object
    :param data: Data that will used to create Twitter Object
                 (Reference Twitter Model for valid field names)
    :return: Boolean - Whether or not creation was successful
    """
    # Check if Twitter Object already exists
    if check_for_existing_twitter_auth(user_id):
        return False
    # Parse data and create dictionary for Twitter Object creation
    # User to associate to Twitter object
    persona_user = persona_model_handler.load_user("id", user_id)
    id = data["id"]
    name = data["name"]
    screen_name = data["screen_name"]
    location = data["location"]
    url = data["url"]
    description = data["description"]
    protected = data.get("protected", False)
    verified = data.get("verified", False)
    followers_count = data.get("followers_count")
    friends_count = data["friends_count"]
    listed_count = data["listed_count"]
    favourites_count = data["favourites_count"]
    statuses_count = data["statuses_count"]
    created_at = data["created_at"]
    profile_image_url = data["profile_image_url"]
    token = data["token"]

    kwargs = {
        "user": persona_user,
        "id": id,
        "name": name,
        "screen_name": screen_name,
        "location": location,
        "url": url,
        "description": description,
        "protected": protected,
        "verified": verified,
        "followers_count": followers_count,
        "friends_count": friends_count,
        "listed_count": listed_count,
        "favourites_count": favourites_count,
        "statuses_count": statuses_count,
        "created_at": created_at,
        "profile_image_url": profile_image_url,
        "token": token
    }

    # Create Twitter Object
    twitter = Twitter(**kwargs)
    try:
        # If Object is valid and able to add to database
        db.session.add(twitter)
        persona_user.twitter_connected = True
        db.session.commit()
        return True
    except Exception as e:
        # If an exception occurs with adding to database
        print("Error adding twitter object to database\n")
        print(e)
        return False


def delete_twitter_object(user_id):
    """
    Delete Twitter Object
    :param user_id: id of User Object
    :return: Boolean - Whether deletion was successful
    """
    twitter = load_object_from_user_id(user_id)
    if twitter is None:
        db.session.delete(twitter)
        db.session.commit()
        return True
    return False


def load_auth_token(user_id):
    tw = Twitter.query.filter_by(user_id=user_id).first()
    if tw is None:
        return None
    oauth_token = tw.oauth_token
    oauth_token_secret = tw.oauth_token_secret
    return {
        "oauth_token": oauth_token,
        "oauth_token_secret": oauth_token_secret
    }


def check_if_in_table(user_id):
    results = Twitter.query.filter_by(user_id=user_id).first()
    if len(results) > 0:
        return True
    return False


def load_object_from_user_id(user_id):
    return Twitter.query.filter_by(user_id=user_id).first()


def check_for_existing_tweet(id):
    tweet = Tweet.query.filter_by(id=id).first()
    if tweet is None:
        return False
    return True


def create_tweet_object(tweet):
    tweet_id = tweet["id"]
    if not check_for_existing_tweet(tweet_id):
        try:
            tweet = Tweet(**tweet)
            db.session.add(tweet)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False
    return False


def create_multiple_tweet_objects(tweets):
    tweet_creation_status = True
    failing_tweets = []
    for tweet in tweets:
        tweet_created = create_tweet_object(tweet)
        if not tweet_created:
            tweet_creation_status = -1
            failing_tweets.append(tweet)
    return tweet_creation_status, failing_tweets


def load_tweets_by_twitter_id(twitter_id):
    return Tweet.query.filter_by(user_id=twitter_id).all()


def load_owned_tweets_by_twitter_id(twitter_id):
    return Tweet.query.filter_by(user_id=twitter_id).filter_by(retweeted=False).all()
