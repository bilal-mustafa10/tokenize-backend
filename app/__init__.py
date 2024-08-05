from config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
import logging
from logging.handlers import RotatingFileHandler
import os

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
jwt = JWTManager()
cors = CORS()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    with app.app_context():
        db.init_app(app)
        migrate.init_app(app, db, compare_type=True)
        ma.init_app(app)
        jwt.init_app(app)
        cors.init_app(app)

    from app.errors import bp as errors_bp
    from app.users import bp as users_bp
    from app.auth import bp as auth_bp
    from app.ai import bp as ai_bp
    from app.smart_contract import bp as smart_contract_bp

    app.register_blueprint(errors_bp)
    app.register_blueprint(users_bp, url_prefix="/api/users")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(ai_bp, url_prefix="/api/ai")
    app.register_blueprint(smart_contract_bp, url_prefix="/api/smart_contract")

    # Set the debuging to rotating log files and the log format and settings
    if not app.debug:
        app.logger.setLevel(logging.INFO)
        app.logger.info("Flask API startup")

    return app
