from __future__ import annotations

import pytest

from communication_api import create_app
from communication_api.config import TestConfig


@pytest.fixture()
def app():
    app = create_app(TestConfig)
    return app


@pytest.fixture()
def client(app):
    return app.test_client()

