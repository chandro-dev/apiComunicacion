from __future__ import annotations

from marshmallow import Schema, fields, validate

from communication_api.domain.enums import Channel


class NotificationRequestSchema(Schema):
    channel = fields.String(
        required=True,
        validate=validate.OneOf([Channel.EMAIL.value, Channel.SMS.value]),
    )
    to = fields.String(required=True, metadata={"description": "Email or phone number"})
    subject = fields.String(load_default=None)
    message = fields.String(required=True)
    metadata = fields.Dict(
        keys=fields.String(),
        values=fields.Raw(),
        load_default=dict,
    )


class NotificationResponseSchema(Schema):
    ok = fields.Boolean(required=True)
    provider = fields.String(required=True)
    channel = fields.String(required=True)
    recipient = fields.String(required=True)
    message_id = fields.String(allow_none=True)
    details = fields.Dict(keys=fields.String(), values=fields.Raw(), required=True)


class HealthResponseSchema(Schema):
    status = fields.String(required=True)
    service = fields.String(required=True)

