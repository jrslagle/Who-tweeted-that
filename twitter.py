import tweepy
from decouple import config
from models import DB, Tweet, User

class Twitter():
    def __init__(self):

        # Authenticate: Key and Secret for OAuth 1
        twitter_key = config('TWITTER_API_KEY', default='OOPS')
        twitter_key_secret = config('TWITTER_API_KEY_SECRET', default='OOPS')
        auth = tweepy.OAuthHandler(twitter_key, twitter_key_secret)
        self.api = tweepy.API(auth)
        # twitter_user = self.api.get_user('katyperry')
        # print(f'{twitter_user.name} (@{twitter_user.screen_name}) has {twitter_user.followers_count:,d} '
        #       f'followers and has made {twitter_user.statuses_count:,d} tweets')
        #
        # tweets = twitter_user.timeline(
        #     count=200, exclue_replies=True, include_rts=False, tweet_mode='extended'
        # )
        # for tweet in tweets[:5]:
        #     print(tweet.full_text)

    def add_or_update_user(self, handle, nlp):
        try:
            twitter_user = self.api.get_user(handle)
            # a handy little user stats printout
            print(f'{twitter_user.name} (@{twitter_user.screen_name}) has {twitter_user.followers_count:,d} '
                  f'followers and has made {twitter_user.statuses_count:,d} tweets')

            # if user isn't in database, create a new one
            db_user = User.query.get(twitter_user.id) or User(id=twitter_user.id, name=handle)


            DB.session.add(db_user)

            tweets = twitter_user.timeline(
                count=200, exclue_replies=True, include_rts=False, tweet_mode='extended'
            )

            for tweet in tweets:
                vectorized_tweet = nlp.tweet_to_vec(tweet.full_text)

                db_tweet = Tweet(id=tweet.id, text=tweet.full_text, vect=vectorized_tweet)

                db_user.tweets.append(db_tweet)
                DB.session.add(db_tweet)
            print(f"Processed {len(tweets)} tweets for @{twitter_user.screen_name}")
        except Exception as e:
            print(e)

        else:
            DB.session.commit()

