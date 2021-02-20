from persona import Tweet
from persona.model_handlers import twitter_model_handler


def calulate_owned_engagement(twitter_id):
    # Load tweets that were actually composed by the user
    owned_tweets = twitter_model_handler.load_owned_tweets_by_twitter_id(twitter_id)
    sorted_tweets = {}
    # Sort tweets based on calculated total engagement
    for tweet in owned_tweets:
        favorite_count = tweet.favorite_count
        retweet_count = tweet.retweet_count
        total_engagement = (1.5 * retweet_count) + (1.0 * favorite_count)
        sorted_tweets[tweet.id] = (total_engagement, tweet)
    # sort tweets by calculated engagement
    return sorted(sorted_tweets.items(), key=lambda item: item[1][0] * -1)
