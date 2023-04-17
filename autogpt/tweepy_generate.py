#!python
import tweepy
import openai
import os

# Authenticate and connect to Twitter API
auth = tweepy.OAuthHandler(
    os.getenv("TWITTER_API_KEY"), os.getenv("TWITTER_API_SECRET_KEY"))
auth.set_access_token(os.getenv("TWITTER_ACCESS_TOKEN"),
                      os.getenv("TWITTER_ACCESS_TOKEN_SECRET"))
api = tweepy.API(auth)

# Authenticate and connect to OpenAI API

openai.api_key = os.getenv('OPENAI_API_KEY')


def post_tweet(tweet_text):
    """
    Posts a tweet to your Twitter timeline.

    Args:
        tweet_text (str): the string of the tweet that will be posted.

    Returns:
        None
    """
    try:
        api.update_status(tweet_text)
        print('Tweeted: ' + tweet_text)
    except tweepy.TweepError as error:
        print(error.reason)


def generate_tweet(prompt):
    """
    Generates a tweet using the OpenAI API.

    Args:
        prompt (str): the prompt for generating the tweet.

    Returns:
        str: the generated tweet text.
    """
    # Set up parameters for OpenAI API
    model_engine = "text-davinci-002"
    model_prompt = prompt + '\nTweet: '
    max_tokens = 50

    # Call OpenAI API to get tweet text
    response = openai.Completion.create(
        model=model_engine,
        prompt=model_prompt,
        max_tokens=max_tokens,
        n=1,
        temperature=0.5)

    tweet_text = response.choices[0].text
    tweet_text = tweet_text.strip().split('Tweet: ')[1].strip()

    return tweet_text

def check_tweet(api, tweet_id):
    """
    Utility function to check the status of a tweet using the Twitter API.
    """
    tweet = api.get_status(tweet_id)
    if tweet.text is not None:
        return True
    else:
        return False
    
def get_tweet_status(api, tweet_id):
    """
    Utility function to retrieve the status of a tweet using the Twitter API.
    """
    tweet = api.get_status(tweet_id, tweet_mode="extended")
    return tweet._json

def get_tweet_likes(api, tweet_id):
    """
    Utility function to retrieve the status of a tweet using the Twitter API.
    """
    tweet = api.get_status(tweet_id, tweet_mode="extended")
    return tweet.favorite_count


def get_latest_tweet() :
    status = api.user_timeline(count=1)[0]
    return status