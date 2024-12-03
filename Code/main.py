from flask import Flask
from Application.database import db
from Application.config import Config

def create_app():
    app=Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    app.app_context().push()
    return app

app=create_app()

from Application.controller import *
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8080
        )
