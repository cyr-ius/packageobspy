"""Class exception."""


class PackageObsException(Exception):
    """Enedis exception."""


class LimitReached(PackageObsException):
    """Limit reached exception."""


class TimeoutExceededError(PackageObsException):
    """Limit reached exception."""


class HttpRequestError(PackageObsException):
    """Http request error."""
