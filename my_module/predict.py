import numpy as np
from sklearn.linear_model import LogisticRegression
from my_module.models import User


def predict_user(user1_handle, user2_handle, tweet_text, nlp):

    user1 = User.query.filter(User.name == user1_handle).first()
    user2 = User.query.filter(User.name == user2_handle).first()

    user1_vectors = np.array([tweet.vect for tweet in user1.tweets])
    user2_vectors = np.array([tweet.vect for tweet in user2.tweets])
    len_user1 = len(user1_vectors)
    len_user2 = len(user2_vectors)
    print(f"Got {len_user1} tweets for {user1.name} and {len_user2} tweets for {user2.name} for a total of {len_user1+len_user2} tweets")

    X = np.vstack([user1_vectors, user2_vectors])
    # X = np.expand_dims(X, axis=1)
    X = X.reshape(-1, 1)
    # X = X.reshape(1, -1)
    y = np.concatenate([np.zeros(len(user1_vectors)),
                        np.ones(len(user2_vectors))])
    print(f"shapes: X = {X.shape}, y = {y.shape}")
    model = LogisticRegression()
    print("initialized the model")
    model.fit(X, y)
    print("fit the model")

    tweet_vect = list(nlp.tweet_to_vec(tweet_text))
    y_pred = model.predict(tweet_vect)
    # return user1_handle if y_pred else user2_handle

    user_map = {0: user1_handle, 1: user2_handle}
    user_name = user_map[y_pred[0]]
    return user_name
