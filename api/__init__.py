from flask import Flask
from flask_pymongo import PyMongo
from flask_apscheduler import APScheduler

from .config import Config

mongo = PyMongo()
scheduler = APScheduler()

def create_app():
    # app instance and config
    app = Flask(__name__)
    app.config.from_object(Config)

    # init extensions
    mongo.app = app
    mongo.init_app(app)
    scheduler.init_app(app)
    scheduler.start()

    return app
