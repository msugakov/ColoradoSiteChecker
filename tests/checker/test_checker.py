import pytest
import aiohttp
from datetime import timedelta
from sitechecker import sitechecker


@pytest.mark.asyncio
async def test_read_http() -> None:
    async with aiohttp.ClientSession() as session:
        result = await sitechecker.read_http(session, "https://cnn.com")
        assert (result.http_status, result.regex_matches, result.error) == (200, None, None)
        assert result.total_time > timedelta()


@pytest.mark.asyncio
async def test_read_http_2() -> None:  # TODO: rename me
    async with aiohttp.ClientSession() as session:
        result = await sitechecker.read_http(session, "https://cnn.com123")
        assert (result.http_status, result.regex_matches) == (None, None)
        assert isinstance(result.error, aiohttp.client_exceptions.ClientConnectorError)
        assert result.total_time > timedelta()
