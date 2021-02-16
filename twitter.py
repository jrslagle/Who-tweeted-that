import tweepy
from decouple import config
import spacy
import pprint

from models import DB, Tweet, User

class Twitter():
    def __init__(self):

        # Authenticate: Key and Secret for OAuth 1
        twitter_key = config('TWITTER_API_KEY', default='OOPS')
        twitter_key_secret = config('TWITTER_API_KEY_SECRET', default='OOPS')
        auth = tweepy.OAuthHandler(twitter_key, twitter_key_secret)
        self.api = tweepy.API(auth)

        # Load English pipeline
        self.nlp = spacy.load('en_core_web_sm')
        # self.nlp = spacy.load('en_core_web_trf')
        # https://spacy.io/models

    # def vectorize_tweet(self, tweet_text):
    #     # nlp = spacy.load('en_core_web_sm')
    #     return self.nlp(tweet.full_text).vector()

    def add_or_update_user(self, handle):
        try:
            twitter_user = self.api.get_user(handle)
            # a handy little user stats printout
            print(f'{twitter_user.screen_name} has {twitter_user.followers_count:,d} followers and has made {twitter_user.statuses_count:,d} tweets')

            # if user isn't in database, create a new one
            db_user = User.query.get(twitter_user.id) or User(id=twitter_user.id, name=handle)
            DB.session.add(db_user)

            tweets = twitter_user.timeline(
                count=200, exclue_replies=True, include_rts=False, tweet_mode='extended'
            )

            for tweet in tweets:
                vectorized_tweet = self.nlp(tweet.full_text).vector()
                doc = self.nlp(tweet.full_text)
                print([(w.text, w.pos_) for w in doc])

                db_tweet = Tweet(id=tweet.id, text=tweet.full_text, vect=vectorized_tweet)
                # db_tweet = Tweet(id=tweet.id, text=tweet.full_text)

                db_user.tweets.append(db_tweet)
                DB.session.add(db_tweet)
        except Exception as e:
            print(e)

        else:
            DB.session.commit()

