class NotificationError(Exception):
    """Base error for the communication API."""


class InputValidationError(NotificationError):
    """Input data is invalid for a channel/provider."""


class ProviderError(NotificationError):
    """Provider failed to deliver the notification."""


class ConfigError(NotificationError):
    """Provider or app configuration is invalid."""

