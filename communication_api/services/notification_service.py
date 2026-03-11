from __future__ import annotations

from communication_api.domain.enums import Channel
from communication_api.domain.models import NotificationPayload, SendResult
from communication_api.exceptions import InputValidationError
from communication_api.factory.provider_factory import NotificationProviderFactory


class NotificationService:
    def __init__(self, provider_factory: NotificationProviderFactory) -> None:
        self.provider_factory = provider_factory

    def send(self, payload: NotificationPayload) -> SendResult:
        self._validate_payload(payload)
        provider = self.provider_factory.create(payload.channel)
        return provider.send(payload)

    @staticmethod
    def _validate_payload(payload: NotificationPayload) -> None:
        if payload.channel == Channel.EMAIL and not payload.subject:
            raise InputValidationError("subject is required when channel=email")

