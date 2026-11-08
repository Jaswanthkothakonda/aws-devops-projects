import os

from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app(test_config=None):
    app = Flask(__name__)

    secret_key = os.getenv("SECRET_KEY")

    if os.getenv("FLASK_ENV") == "production" and not secret_key:
        raise RuntimeError("SECRET_KEY must be set in production")

    app.config["SECRET_KEY"] = secret_key or "unsafe-development-key"
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite:///beasteats.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    migrate.init_app(app, db)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    from app.routes import main
    from app.auth import auth

    app.register_blueprint(main)
    app.register_blueprint(auth)

    return app
