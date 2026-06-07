# packageobspy

An async Python library to retrieve weather observation packages from the [Météo-France public API](https://portail-api.meteofrance.fr).

## Features

- Fetch the list of all available weather stations
- Retrieve 6-minute intra-hourly observation packages by station ID
- Retrieve hourly observation packages by department (covering the last 24 hours)
- Automatic OAuth2 token management (client credentials flow, with expiry handling)
- Fully asynchronous — built on `aiohttp`

## Requirements

- Python >= 3.11
- `aiohttp` >= 3.9.5
- A Météo-France API token (Base64-encoded `client_id:client_secret`)

## Installation

```bash
pip install packageobspy
```

## Quick Start

```python
import asyncio
from aiohttp import ClientSession
from packageobspy import PackageObs

async def main():
    async with ClientSession() as session:
        api = PackageObs(token="<your_base64_token>", session=session)

        # List all available stations
        stations = await api.async_get_stations()

        # Get 6-minute observations for a station
        obs_6m = await api.async_get_6m(id_station=98833002)

        # Get hourly observations for a department (e.g., Yvelines = 78)
        obs_hourly = await api.async_get_horaire(id_departement=78)

        print(obs_6m)

asyncio.run(main())
```

The `PackageObs` class also supports the async context manager protocol:

```python
async with PackageObs(token="<your_base64_token>", session=session) as api:
    stations = await api.async_get_stations()
```

## API Reference

### `PackageObs(token, session, timeout)`

| Parameter | Type                    | Default     | Description                                                       |
| --------- | ----------------------- | ----------- | ----------------------------------------------------------------- |
| `token`   | `str`                   | required    | Base64-encoded `client_id:client_secret` for the Météo-France API |
| `session` | `aiohttp.ClientSession` | new session | An existing `aiohttp` client session                              |
| `timeout` | `int`                   | `30`        | Request timeout in seconds                                        |

### Methods

| Method                              | Description                                                         |
| ----------------------------------- | ------------------------------------------------------------------- |
| `async_get_stations()`              | Returns the list of all observation stations                        |
| `async_get_6m(id_station)`          | Returns the latest 6-minute observation package for a station       |
| `async_get_horaire(id_departement)` | Returns the hourly observation package for a department (last 24 h) |
| `async_close()`                     | Closes the underlying HTTP session                                  |

## Exceptions

| Exception              | Description                                      |
| ---------------------- | ------------------------------------------------ |
| `PackageObsException`  | Base exception for all library errors            |
| `HttpRequestError`     | Raised when a network or connection error occurs |
| `TimeoutExceededError` | Raised when the request times out                |
| `LimitReached`         | Raised when the API rate limit is reached        |

## Getting an API Token

1. Register at [portail-api.meteofrance.fr](https://portail-api.meteofrance.fr).
2. Subscribe to the **DPPaquetObs** product.
3. Retrieve your `client_id` and `client_secret`.
4. Base64-encode them as `client_id:client_secret` and pass the result as `token`.

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE).
