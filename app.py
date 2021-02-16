from flask import Flask, render_template
from models import DB, User  # , insert_data
from twitter import Twitter


def create_app():

    app = Flask("Twitoff-james-slagle")

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    DB.init_app(app)

    twitter = Twitter()

    @app.route("/")
    def landing():
        DB.drop_all()
        DB.create_all()
        # example_users = ['elonmusk', 'katyperry', 'rihanna', 'barackobama', 'Hitch_Slapping']
        example_users = ['katyperry']
        for user in example_users:
            twitter.add_or_update_user(user)
        return render_template("home.html", title="Lambda3.3.1", users=User.query.all())

    @app.route("/update")
    def update():
        return render_template("home.html", title="Lambda3.3.1", users=User.query.all())

    @app.route("/reset")
    def reset():
        return render_template("home.html", title="Lambda3.3.1", users=User.query.all())

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
