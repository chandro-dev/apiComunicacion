from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    API_TITLE = "Communication API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    EMAIL_PROVIDER = os.getenv("EMAIL_PROVIDER", "console")
    SMS_PROVIDER = os.getenv("SMS_PROVIDER", "console")

    SMTP_HOST = os.getenv("SMTP_HOST", "")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    SMTP_FROM = os.getenv("SMTP_FROM", "")
    SMTP_TIMEOUT_SECONDS = float(os.getenv("SMTP_TIMEOUT_SECONDS", "10"))

    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
    TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER", "")
    TWILIO_MESSAGING_SERVICE_SID = os.getenv("TWILIO_MESSAGING_SERVICE_SID", "")
    TWILIO_TIMEOUT_SECONDS = float(os.getenv("TWILIO_TIMEOUT_SECONDS", "10"))


class TestConfig(BaseConfig):
    TESTING = True
    EMAIL_PROVIDER = "console"
    SMS_PROVIDER = "console"
