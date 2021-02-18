from flask import Flask, render_template, request
import time
import numpy as np
import logging
from my_module.models import DB, User  # , insert_data
from my_module.twitter import Twitter
from my_module.nlp_model import NLP
from my_module.predict import predict_user


def create_app():

    app = Flask(__name__)
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    DB.init_app(app)
    twitter = Twitter()
    times = [time.time()]
    nlp = NLP()
    times.append(time.time())
    times = np.array(times)-times[0]
    print(f"Loading times: {times}")

    @app.route("/", methods=['GET'])
    def landing():
        DB.drop_all()
        DB.create_all()
        example_users = ['elonmusk',  # Elon Musk
                         'rihanna',  # Rihanna
                         'barackobama',  # Barack Obama
                         'katyperry',  # KATY PERRY
                         'Hitch_Slapping',  # Christopher Hitchens quotes
                         'SamMakingSense',  # Sam Harris quotes
                         'RWEmersonQuotes',  # Ralph Waldo Emerson quotes
                         ]
        for user in example_users:
            twitter.add_or_update_user(user, nlp)
        return render_template("home.html", title="Lambda3.3.1", users=User.query.all())

    @app.route("/update")
    def update():
        return render_template("home.html", title="Lambda3.3.1", users=User.query.all())

    @app.route("/reset")
    def reset():
        return render_template("home.html", title="Lambda3.3.1", users=User.query.all())

    @app.route("/compare", methods=['POST'])
    def compare():
        user1 = request.form['selected_user_1']
        user2 = request.form['selected_user_2']
        tweet_text = request.values['tweet_text']
        if user1 == user2:
            message = 'Cannot compare the same user to itself'
        else:
            prediction = predict_user(user1, user2, tweet_text, nlp)
            message = f"{prediction} is more likely to have said {tweet_text}"
        return render_template('prediction.html', title='Predict Tweet Author', message=message)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
