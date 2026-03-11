from __future__ import annotations

import requests

from communication_api.domain.models import NotificationPayload, SendResult
from communication_api.exceptions import ConfigError, ProviderError
from communication_api.providers.base import NotificationProvider


class TwilioSmsProvider(NotificationProvider):
    def __init__(
        self,
        account_sid: str,
        auth_token: str,
        from_number: str | None = None,
        messaging_service_sid: str | None = None,
        timeout_seconds: float = 10,
    ) -> None:
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.from_number = from_number or None
        self.messaging_service_sid = messaging_service_sid or None
        self.timeout_seconds = timeout_seconds

        missing = []
        if not self.account_sid:
            missing.append("TWILIO_ACCOUNT_SID")
        if not self.auth_token:
            missing.append("TWILIO_AUTH_TOKEN")
        if missing:
            raise ConfigError(f"Twilio provider misconfigured. Missing: {', '.join(missing)}")

        if not self.from_number and not self.messaging_service_sid:
            raise ConfigError(
                "Twilio requires TWILIO_FROM_NUMBER or TWILIO_MESSAGING_SERVICE_SID"
            )

    @property
    def provider_name(self) -> str:
        return "twilio-sms"

    def send(self, payload: NotificationPayload) -> SendResult:
        endpoint = (
            f"https://api.twilio.com/2010-04-01/Accounts/{self.account_sid}/Messages.json"
        )
        body: dict[str, str] = {
            "To": payload.recipient,
            "Body": payload.message,
        }
        if self.messaging_service_sid:
            body["MessagingServiceSid"] = self.messaging_service_sid
        elif self.from_number:
            body["From"] = self.from_number

        status_callback = payload.metadata.get("status_callback")
        if status_callback:
            body["StatusCallback"] = str(status_callback)

        try:
            response = requests.post(
                endpoint,
                data=body,
                auth=(self.account_sid, self.auth_token),
                timeout=self.timeout_seconds,
            )
            if response.status_code >= 400:
                raise ProviderError(
                    f"Twilio send failed ({response.status_code}): {response.text}"
                )
            data = response.json()
        except requests.RequestException as exc:
            raise ProviderError(f"Twilio request failed: {exc}") from exc

        return SendResult(
            ok=True,
            provider=self.provider_name,
            channel=payload.channel,
            recipient=payload.recipient,
            message_id=data.get("sid"),
            details={
                "status": data.get("status"),
                "direction": data.get("direction"),
                "trial_note": "Trial accounts can send only to verified numbers.",
            },
        )

