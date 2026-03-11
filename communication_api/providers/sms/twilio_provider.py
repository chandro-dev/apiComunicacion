from __future__ import annotations

from communication_api.domain.models import NotificationPayload, SendResult
from communication_api.exceptions import ConfigError, ProviderError
from communication_api.providers.base import NotificationProvider
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client


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
        self.client = Client(self.account_sid, self.auth_token)

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
        body: dict[str, str] = {
            "to": payload.recipient,
            "body": payload.message,
        }
        if self.messaging_service_sid:
            body["messaging_service_sid"] = self.messaging_service_sid
        elif self.from_number:
            body["from_"] = self.from_number

        status_callback = payload.metadata.get("status_callback")
        if status_callback:
            body["status_callback"] = str(status_callback)

        try:
            message = self.client.messages.create(**body)
        except TwilioRestException as exc:
            raise ProviderError(f"Twilio send failed ({exc.code}): {exc.msg}") from exc
        except Exception as exc:  # noqa: BLE001
            raise ProviderError(f"Twilio request failed: {exc}") from exc

        return SendResult(
            ok=True,
            provider=self.provider_name,
            channel=payload.channel,
            recipient=payload.recipient,
            message_id=message.sid,
            details={
                "status": message.status,
                "direction": message.direction,
                "trial_note": "Trial accounts can send only to verified numbers.",
            },
        )
