from __future__ import annotations

import pytest

from communication_api.domain.enums import Channel
from communication_api.domain.models import NotificationPayload
from communication_api.exceptions import ConfigError
from communication_api.providers.sms.twilio_provider import TwilioSmsProvider


def test_twilio_requires_sender_or_messaging_service() -> None:
    with pytest.raises(ConfigError):
        TwilioSmsProvider(
            account_sid="AC123",
            auth_token="token",
            from_number="",
            messaging_service_sid="",
        )


def test_twilio_send_success(monkeypatch: pytest.MonkeyPatch) -> None:
    class DummyMessage:
        sid = "SM123"
        status = "queued"
        direction = "outbound-api"

    class DummyMessages:
        @staticmethod
        def create(**kwargs) -> DummyMessage:  # noqa: ANN003
            return DummyMessage()

    class DummyClient:
        messages = DummyMessages()

    monkeypatch.setattr(
        "communication_api.providers.sms.twilio_provider.Client",
        lambda *args, **kwargs: DummyClient(),  # noqa: ARG005
    )

    provider = TwilioSmsProvider(
        account_sid="AC123",
        auth_token="token",
        from_number="+15005550006",
    )
    result = provider.send(
        NotificationPayload(
            channel=Channel.SMS,
            recipient="+573001112233",
            message="Hola",
        )
    )

    assert result.ok is True
    assert result.message_id == "SM123"
    assert result.provider == "twilio-sms"
