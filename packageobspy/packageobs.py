"""Class for MyRain."""

from __future__ import annotations

import logging
from typing import Any

from aiohttp import ClientSession

from .auth import Auth
from .const import API_URL, TIMEOUT

_LOGGER = logging.getLogger(__name__)


class PackageObs:
    """Get data of pdl."""

    def __init__(
        self,
        token: str,
        session: ClientSession = ClientSession(),
        timeout: int = TIMEOUT,
    ) -> None:
        """Initialize."""
        self.auth = Auth(token, session, timeout)

    async def async_get_stations(self) -> Any:
        """List stations."""
        service = "DPPaquetObs/v1/liste-stations?format=json"
        return await self.auth.async_request(url=f"{API_URL}/{service}", method="get")

    async def async_get_6m(self, id_station: int) -> Any:
        """Get observations package by station id."""
        service = (
            f"DPPaquetObs/v1/paquet/infrahoraire-6m?id_station={id_station}&format=json"
        )
        return await self.auth.async_request(url=f"{API_URL}/{service}", method="get")

    async def async_get_horaire(self, id_departement: int) -> Any:
        """Get observations package by department (24h)."""
        service = (
            f"DPPaquetObs/v1/paquet/horaire?id-departement={id_departement}&format=json"
        )
        return await self.auth.async_request(url=f"{API_URL}/{service}", method="get")

    async def async_close(self) -> None:
        """Close the session."""
        if self.auth.session:
            await self.auth.session.close()

    async def __aenter__(self) -> PackageObs:
        """Asynchronous enter."""
        return self

    async def __aexit__(self, *_exc_info: object) -> None:
        """Async exit."""
        await self.async_close()
