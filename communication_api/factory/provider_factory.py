from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from communication_api.domain.enums import Channel
from communication_api.exceptions import ConfigError
from communication_api.providers.base import NotificationProvider
from communication_api.providers.email.console_provider import ConsoleEmailProvider
from communication_api.providers.email.smtp_provider import SMTPEmailProvider
from communication_api.providers.sms.console_provider import ConsoleSmsProvider
from communication_api.providers.sms.twilio_provider import TwilioSmsProvider


class NotificationProviderFactory:
    def __init__(self, config: Mapping[str, Any]) -> None:
        self.config = config

    def create(self, channel: Channel) -> NotificationProvider:
        if channel == Channel.EMAIL:
            return self._build_email_provider()
        if channel == Channel.SMS:
            return self._build_sms_provider()
        raise ConfigError(f"Unsupported channel: {channel}")

    def _build_email_provider(self) -> NotificationProvider:
        name = str(self.config.get("EMAIL_PROVIDER", "console")).strip().lower()
        if name == "console":
            return ConsoleEmailProvider()
        if name == "smtp":
            return SMTPEmailProvider(
                host=str(self.config.get("SMTP_HOST", "")),
                port=int(self.config.get("SMTP_PORT", 587)),
                username=str(self.config.get("SMTP_USERNAME", "")),
                password=str(self.config.get("SMTP_PASSWORD", "")),
                sender=str(self.config.get("SMTP_FROM", "")),
                timeout_seconds=float(self.config.get("SMTP_TIMEOUT_SECONDS", 10)),
            )
        raise ConfigError(f"EMAIL_PROVIDER '{name}' is not supported")

    def _build_sms_provider(self) -> NotificationProvider:
        name = str(self.config.get("SMS_PROVIDER", "console")).strip().lower()
        if name == "console":
            return ConsoleSmsProvider()
        if name in {"twilio", "twilio_sms"}:
            return TwilioSmsProvider(
                account_sid=str(self.config.get("TWILIO_ACCOUNT_SID", "")),
                auth_token=str(self.config.get("TWILIO_AUTH_TOKEN", "")),
                from_number=str(self.config.get("TWILIO_FROM_NUMBER", "")),
                messaging_service_sid=str(
                    self.config.get("TWILIO_MESSAGING_SERVICE_SID", "")
                ),
                timeout_seconds=float(self.config.get("TWILIO_TIMEOUT_SECONDS", 10)),
            )
        raise ConfigError(f"SMS_PROVIDER '{name}' is not supported")
