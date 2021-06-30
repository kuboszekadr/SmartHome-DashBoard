from flask import Flask

pages = []

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    with app.app_context():
        return app