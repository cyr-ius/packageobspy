"""Class for Authentication."""

from __future__ import annotations

import asyncio
from datetime import datetime as dt, timedelta
import json
import logging
import socket
from typing import Any

from aiohttp import ClientError, ClientResponseError, ClientSession

from .const import TIMEOUT, TOKEN_ENDPONT
from .exceptions import HttpRequestError, PackageObsException, TimeoutExceededError

_LOGGER = logging.getLogger(__name__)


class Auth:
    """Class for Auth API."""

    def __init__(
        self, token: str, session: ClientSession, timeout: int = TIMEOUT
    ) -> None:
        """Init."""
        self.token = token
        self.timeout = timeout
        self.session = session
        self.last_access: dt | None = None
        self.access_token: str | None = None
        self.expires_in: dt = dt.now()

    async def async_request(self, url: str, method: str = "get", **kwargs: Any) -> Any:
        """Request session."""
        kwargs.setdefault("headers", {})

        if url != TOKEN_ENDPONT:
            await self.async_get_token()
            kwargs["headers"] = {"Authorization": f"Bearer {self.access_token}"}

        try:
            async with asyncio.timeout(TIMEOUT):
                _LOGGER.debug("Request: %s (%s) - %s", url, method, kwargs.get("json"))
                response = await self.session.request(method, url, **kwargs)
                contents = await response.read()
                response.raise_for_status()
        except (asyncio.CancelledError, asyncio.TimeoutError) as error:
            raise TimeoutExceededError(
                "Timeout occurred while connecting to MyRain."
            ) from error
        except ClientResponseError:
            if "application/json" in response.headers.get("Content-Type", ""):
                raise PackageObsException(
                    response.status, json.loads(contents.decode("utf8"))
                )
            raise PackageObsException(response.status, {"message": contents})
        except (ClientError, socket.gaierror) as error:
            raise HttpRequestError(
                "Error occurred while communicating with MyRain."
            ) from error

        return (
            await response.json()
            if "application/json" in response.headers.get("Content-Type", "")
            else await response.text()
        )

    async def async_get_token(self) -> None:
        if dt.now() > self.expires_in:
            token = await self.async_request(
                url=TOKEN_ENDPONT,
                method="post",
                json={"grant_type": "client_credentials"},
                headers={"Authorization": f"Basic {self.token}"},
            )
            self.expires_in = dt.now() + timedelta(seconds=token["expires_in"])
            self.access_token = token["access_token"]
