"""HTTP request handler for the PackageObs API client."""

import asyncio
from datetime import datetime as dt, timedelta
import json
import logging
import socket
from typing import Any

from aiohttp import ClientError, ClientResponseError, ClientSession

from .const import TIMEOUT, TOKEN_ENDPONT
from .exceptions import PackageObsException

_LOGGER = logging.getLogger(__name__)


class HTTPRequest:
    """Base class handling authenticated HTTP requests."""

    def __init__(
        self, token: str, session: ClientSession | None = None, timeout: int = TIMEOUT
    ) -> None:
        """Initialize the HTTP request handler with credentials and session options."""
        self.token = token
        self.timeout = timeout
        self.session = session or ClientSession()
        self.last_access: dt | None = None
        self.access_token: str | None = None
        self.expires_in: dt = dt.now()

    async def async_request(self, url: str, method: str = "get", **kwargs: Any) -> Any:
        """Send an authenticated HTTP request and return the parsed response."""
        contents: Any = None
        response: Any = None
        kwargs.setdefault("headers", {})

        if url != TOKEN_ENDPONT:
            await self.async_get_token()
            kwargs["headers"] = {"Authorization": f"Bearer {self.access_token}"}

        try:
            async with asyncio.timeout(TIMEOUT):
                if self.session is None:
                    raise HttpRequestError("ClientSession is not initialized.")
                _LOGGER.debug("Request: %s (%s) - %s", url, method, kwargs.get("json"))
                response = await self.session.request(method, url, **kwargs)
                contents = await response.read()
                response.raise_for_status()
        except (asyncio.CancelledError, asyncio.TimeoutError) as error:
            raise TimeoutExceededError(
                "Timeout occurred while connecting to PackageObs API."
            ) from error
        except ClientResponseError:
            if "application/json" in response.headers.get("Content-Type", ""):
                raise PackageObsException(
                    response.status, json.loads(contents.decode("utf8"))
                )
            raise PackageObsException(response.status, {"message": contents})
        except (ClientError, socket.gaierror) as error:
            raise HttpRequestError(
                "Error occurred while communicating with PackageObs API."
            ) from error

        return (
            await response.json()
            if "application/json" in response.headers.get("Content-Type", "")
            else await response.text()
        )

    async def async_get_token(self) -> None:
        """Fetch and cache a new OAuth2 access token if the current one has expired."""
        if dt.now() > self.expires_in:
            token = await self.async_request(
                url=TOKEN_ENDPONT,
                method="post",
                json={"grant_type": "client_credentials"},
                headers={"Authorization": f"Basic {self.token}"},
            )
            self.expires_in = dt.now() + timedelta(seconds=token["expires_in"])
            self.access_token = token["access_token"]

    async def async_close(self) -> None:
        """Close the HTTP session."""
        if self.session:
            await self.session.close()
            self.session = None


class HttpRequestError(Exception):
    """Base exception for HTTP request errors."""


class TimeoutExceededError(HttpRequestError):
    """Exception raised when a request times out."""


class RequestException(HttpRequestError):
    """Exception raised for errors in the request."""
