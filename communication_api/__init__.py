from __future__ import annotations

from flask import Flask
from dotenv import load_dotenv

from communication_api.api.health import blp as health_blueprint
from communication_api.api.notifications import blp as notifications_blueprint
from communication_api.config import BaseConfig
from communication_api.extensions import api


def create_app(config_object: type[BaseConfig] | None = None) -> Flask:
    load_dotenv(".env")
    app = Flask(__name__)
    app.config.from_object(config_object or BaseConfig)

    api.init_app(app)
    api.register_blueprint(health_blueprint)
    api.register_blueprint(notifications_blueprint)

    return app
