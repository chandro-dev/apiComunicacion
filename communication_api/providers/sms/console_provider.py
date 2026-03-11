from __future__ import annotations

import logging

from communication_api.domain.models import NotificationPayload, SendResult
from communication_api.providers.base import NotificationProvider

logger = logging.getLogger(__name__)


class ConsoleSmsProvider(NotificationProvider):
    @property
    def provider_name(self) -> str:
        return "console-sms"

    def send(self, payload: NotificationPayload) -> SendResult:
        logger.info(
            "SMS(console) to=%s message=%s metadata=%s",
            payload.recipient,
            payload.message,
            payload.metadata,
        )
        return SendResult(
            ok=True,
            provider=self.provider_name,
            channel=payload.channel,
            recipient=payload.recipient,
            details={"mode": "console"},
        )

