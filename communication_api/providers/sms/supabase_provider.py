from __future__ import annotations

import requests

from communication_api.domain.models import NotificationPayload, SendResult
from communication_api.exceptions import ConfigError, ProviderError
from communication_api.providers.base import NotificationProvider


class SupabaseOtpSmsProvider(NotificationProvider):
    """
    Supabase Auth only supports OTP-style SMS.
    It does not send arbitrary custom message text.
    """

    def __init__(
        self,
        base_url: str,
        service_role_key: str,
        create_user: bool = True,
        timeout_seconds: float = 10,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.service_role_key = service_role_key
        self.create_user = create_user
        self.timeout_seconds = timeout_seconds

        missing = []
        if not self.base_url:
            missing.append("SUPABASE_URL")
        if not self.service_role_key:
            missing.append("SUPABASE_SERVICE_ROLE_KEY")
        if missing:
            raise ConfigError(
                f"Supabase OTP provider misconfigured. Missing: {', '.join(missing)}"
            )

    @property
    def provider_name(self) -> str:
        return "supabase-otp-sms"

    def send(self, payload: NotificationPayload) -> SendResult:
        endpoint = f"{self.base_url}/auth/v1/otp"
        headers = {
            "apikey": self.service_role_key,
            "Authorization": f"Bearer {self.service_role_key}",
            "Content-Type": "application/json",
        }
        body = {
            "phone": payload.recipient,
            "channel": "sms",
            "create_user": self.create_user,
        }

        try:
            response = requests.post(
                endpoint, json=body, headers=headers, timeout=self.timeout_seconds
            )
            if response.status_code >= 400:
                raise ProviderError(
                    f"Supabase OTP send failed ({response.status_code}): {response.text}"
                )
            data = response.json() if response.text else {}
        except requests.RequestException as exc:
            raise ProviderError(f"Supabase request failed: {exc}") from exc

        return SendResult(
            ok=True,
            provider=self.provider_name,
            channel=payload.channel,
            recipient=payload.recipient,
            message_id=data.get("id"),
            details={
                "warning": "Supabase OTP ignores custom message content.",
                "supabase_response": data,
            },
        )

