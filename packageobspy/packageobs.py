"""PackageObs client for Météo-France observation data."""

from __future__ import annotations

import logging
from typing import Any

from aiohttp import ClientSession

from .auth import HTTPRequest, HttpRequestError
from .const import API_URL, TIMEOUT
from .exceptions import PackageObsException

_LOGGER = logging.getLogger(__name__)


class PackageObs(HTTPRequest):
    """Client for the Météo-France DPPaquetObs observation API."""

    def __init__(
        self, token: str, session: ClientSession | None = None, timeout: int = TIMEOUT
    ) -> None:
        """Initialize."""
        super().__init__(token=token, session=session, timeout=timeout)

    async def async_get_stations(self) -> Any:
        """List stations."""
        service = "DPPaquetObs/v1/liste-stations?format=json"
        try:
            return await self.async_request(url=f"{API_URL}/{service}", method="get")
        except HttpRequestError as err:
            _LOGGER.error("Failed to fetch station list: %s", err)
            raise PackageObsException(err) from err

    async def async_get_6m(self, id_station: int) -> Any:
        """Get observations package by station id."""
        service = (
            f"DPPaquetObs/v1/paquet/infrahoraire-6m?id_station={id_station}&format=json"
        )
        try:
            return await self.async_request(url=f"{API_URL}/{service}", method="get")
        except HttpRequestError as err:
            _LOGGER.error(
                "Failed to fetch 6-min observations for station %s: %s", id_station, err
            )
            raise PackageObsException(err) from err

    async def async_get_horaire(self, id_departement: int) -> Any:
        """Get observations package by department (24h)."""
        service = (
            f"DPPaquetObs/v1/paquet/horaire?id-departement={id_departement}&format=json"
        )
        try:
            return await self.async_request(url=f"{API_URL}/{service}", method="get")
        except HttpRequestError as err:
            _LOGGER.error(
                "Failed to fetch hourly observations for department %s: %s",
                id_departement,
                err,
            )
            raise PackageObsException(err) from err
