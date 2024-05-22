#!/usr/bin/env python3
"""Example code."""

import asyncio
import logging

from aiohttp import ClientSession
import yaml

from packageobspy import PackageObs

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# create console handler and set level to debug
ch = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)

# Fill out the secrets in secrets.yaml, you can find an example
# _secrets.yaml file, which has to be renamed after filling out the secrets.
with open("./secrets.yaml", encoding="UTF-8") as file:
    secrets = yaml.safe_load(file)


async def main() -> None:
    """Main function."""
    async with ClientSession() as session:
        api = PackageObs(token=secrets["TOKEN"], session=session)
        response = await api.async_get_stations()
        response = await api.async_get_6m(id_station=72181001)
        response = await api.async_get_horaire(id_departement=72)
        logger.info(response)
        await api.async_close()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run(main())
