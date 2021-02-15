import tweepy
from decouple import config
# import spacy
# import pprint

from models import DB, Tweet, User

class Twitter():
    def __init__(self):

        # Authenticate: Key and Secret for OAuth 1
        twitter_key = config('TWITTER_API_KEY', default='OOPS')
        twitter_key_secret = config('TWITTER_API_KEY_SECRET', default='OOPS')

        # Authenticate: Generate a Bearer Token
        auth = tweepy.OAuthHandler(twitter_key, twitter_key_secret)
        self.api = tweepy.API(auth)


        # twitter_user = self.api.get_user('katyperry')
        # tweets = twitter_user.timeline(
        #     count=50, exclue_replies=True, include_rts=False, tweet_mode='extended'
        # )
        # for tweet in tweets:
        #     print(tweet.full_text)

        # nlp = spacy.load('my_model')

    # def vectorize_tweet(tweet_text):
        # return nlp(tweet_text).vector()

    def add_or_update_user(self, handle):
        try:
            twitter_user = self.api.get_user(handle)
            db_user = User.query.get(twitter_user.id) or User(id=twitter_user.id, name=handle)
            DB.session.add(db_user)

            tweets = twitter_user.timeline(
                count=200, exclue_replies=True, include_rts=False, tweet_mode='extended'
            )
            for tweet in tweets:
                # vectorized_tweet = vectorize_tweet(tweet.full_text)

                # db_tweet = Tweet(id=tweet.id, text=tweet.full_text, vect=vectorized_tweet)
                db_tweet = Tweet(id=tweet.id, text=tweet.full_text)

                db_user.tweets.append(db_tweet)
                DB.session.add(db_tweet)
        except Exception as e:
            print(e)

        else:
            DB.session.commit()

