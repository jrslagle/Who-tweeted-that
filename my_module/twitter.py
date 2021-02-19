import tweepy
from decouple import config
from my_module.models import DB, Tweet, User

class Twitter():
    def __init__(self):

        # Authenticate: Key and Secret for OAuth 1
        twitter_key = config('TWITTER_API_KEY', default='OOPS')
        twitter_key_secret = config('TWITTER_API_KEY_SECRET', default='OOPS')
        auth = tweepy.OAuthHandler(twitter_key, twitter_key_secret)
        self.api = tweepy.API(auth)

    def add_or_update_user(self, handle, nlp):
        try:
            twitter_user = self.api.get_user(handle)
            # a handy little user stats printout
            # print(f'{twitter_user.name} (@{twitter_user.screen_name}) has {twitter_user.followers_count:,d} '
            #       f'followers and has made {twitter_user.statuses_count:,d} tweets')

            # The old method
            # db_user = User.query.get(twitter_user.id) or User(id=twitter_user.id, name=handle)

            # existing_user = User.query.get(twitter_user.id)
            # existing_user = User.query.get(handle)
            # existing_user = User.query.filter(User.name == handle).first()
            existing_user = User.query.filter(User.name == handle).first()
            print(f'fetching handle {handle} and found {existing_user}')
            # print(f"existing user = {existing_user}")

            if existing_user:
                pass
            else:
                # if user isn't in database, create a new one
                new_user = User(id=twitter_user.id, name=handle)
                # print(f"new user = {new_user}")

                DB.session.add(new_user)

                tweets = twitter_user.timeline(
                    count=200, exclue_replies=True, include_rts=False, tweet_mode='extended'
                )

                for tweet in tweets:
                    vectorized_tweet = nlp.tweet_to_vec(tweet.full_text)

                    db_tweet = Tweet(id=tweet.id, text=tweet.full_text, vect=vectorized_tweet)

                    new_user.tweets.append(db_tweet)
                    DB.session.add(db_tweet)
                print(f"Processed {len(tweets)} tweets for @{twitter_user.screen_name}")
        except Exception as e:
            print(e)

        else:
            DB.session.commit()

