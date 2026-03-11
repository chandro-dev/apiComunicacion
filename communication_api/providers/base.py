from __future__ import annotations

from abc import ABC, abstractmethod

from communication_api.domain.models import NotificationPayload, SendResult


class NotificationProvider(ABC):
    @property
    @abstractmethod
    def provider_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def send(self, payload: NotificationPayload) -> SendResult:
        raise NotImplementedError

