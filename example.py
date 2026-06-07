#!/usr/bin/env python3
"""Example code."""

import asyncio
import logging

from aiohttp import ClientSession
import yaml

from packageobspy import PackageObs, PackageObsException

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


async def async_main() -> None:
    """Main function."""
    async with ClientSession() as session:
        api = PackageObs(token=secrets["TOKEN"], session=session)
        try:
            logger.info(await api.async_get_stations())
            logger.info(await api.async_get_6m(id_station=98833002))
            logger.info(await api.async_get_horaire(id_departement=78))
        except PackageObsException as err:
            logger.error(err)
        finally:
            await api.async_close()


if __name__ == "__main__":
    asyncio.run(async_main())
