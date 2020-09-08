from flask import Flask
from flask_bootstrap import Bootstrap

pages = []

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    from . import index, aquarium, solar
    app.register_blueprint(index.bp)
    app.register_blueprint(aquarium.bp)
    app.register_blueprint(solar.bp)

    Bootstrap(app)
    return app