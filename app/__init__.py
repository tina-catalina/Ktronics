from flask import Flask
from .modules.auth import auth
from .modules.db import db

def create_app():
    app = Flask(__name__, template_folder="templates")
    app.register_blueprint(auth)
    app.register_blueprint(db)

    return app