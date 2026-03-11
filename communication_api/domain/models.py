from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from communication_api.domain.enums import Channel


@dataclass(slots=True)
class NotificationPayload:
    channel: Channel
    recipient: str
    message: str
    subject: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class SendResult:
    ok: bool
    provider: str
    channel: Channel
    recipient: str
    message_id: str | None = None
    details: dict[str, Any] = field(default_factory=dict)

