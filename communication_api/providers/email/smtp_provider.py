from __future__ import annotations

import smtplib
from email.message import EmailMessage

from communication_api.domain.models import NotificationPayload, SendResult
from communication_api.exceptions import ConfigError, ProviderError
from communication_api.providers.base import NotificationProvider


class SMTPEmailProvider(NotificationProvider):
    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        sender: str,
        timeout_seconds: float = 10,
    ) -> None:
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.sender = sender
        self.timeout_seconds = timeout_seconds

        missing = []
        if not self.host:
            missing.append("SMTP_HOST")
        if not self.username:
            missing.append("SMTP_USERNAME")
        if not self.password:
            missing.append("SMTP_PASSWORD")
        if not self.sender:
            missing.append("SMTP_FROM")

        if missing:
            raise ConfigError(f"SMTP provider misconfigured. Missing: {', '.join(missing)}")

    @property
    def provider_name(self) -> str:
        return "smtp"

    def send(self, payload: NotificationPayload) -> SendResult:
        subject = payload.subject or "(Sin asunto)"
        email = EmailMessage()
        email["From"] = self.sender
        email["To"] = payload.recipient
        email["Subject"] = subject
        email.set_content(payload.message)

        try:
            with smtplib.SMTP(self.host, self.port, timeout=self.timeout_seconds) as smtp:
                smtp.starttls()
                smtp.login(self.username, self.password)
                smtp.send_message(email)
        except Exception as exc:  # noqa: BLE001
            raise ProviderError(f"SMTP send failed: {exc}") from exc

        return SendResult(
            ok=True,
            provider=self.provider_name,
            channel=payload.channel,
            recipient=payload.recipient,
            details={"subject": subject},
        )

