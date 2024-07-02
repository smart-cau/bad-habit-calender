from flask import Flask, render_template


def create_app():
    app = Flask(__name__)

    # init extensions

    # import and register blueprints
    @app.route("/")
    def hello_world():
        return render_template("index.html")

    # custom error handlers

    return app
