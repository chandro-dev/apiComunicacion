from __future__ import annotations

from flask import current_app
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from communication_api.domain.enums import Channel
from communication_api.domain.models import NotificationPayload
from communication_api.exceptions import ConfigError, InputValidationError, ProviderError
from communication_api.factory.provider_factory import NotificationProviderFactory
from communication_api.schemas import NotificationRequestSchema, NotificationResponseSchema
from communication_api.services.notification_service import NotificationService

blp = Blueprint("notifications", __name__, description="Notification endpoints")


@blp.route("/api/v1/notifications/send")
class NotificationSendResource(MethodView):
    @blp.arguments(NotificationRequestSchema)
    @blp.response(200, NotificationResponseSchema)
    def post(self, data: dict) -> dict:
        payload = NotificationPayload(
            channel=Channel(data["channel"]),
            recipient=data["to"],
            subject=data.get("subject"),
            message=data["message"],
            metadata=data.get("metadata", {}),
        )
        service = NotificationService(NotificationProviderFactory(current_app.config))
        try:
            result = service.send(payload)
            return {
                "ok": result.ok,
                "provider": result.provider,
                "channel": result.channel.value,
                "recipient": result.recipient,
                "message_id": result.message_id,
                "details": result.details,
            }
        except InputValidationError as exc:
            abort(400, message=str(exc))
        except ConfigError as exc:
            abort(500, message=str(exc))
        except ProviderError as exc:
            abort(502, message=str(exc))

