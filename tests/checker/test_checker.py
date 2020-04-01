from datetime import timedelta

import aiohttp
import pytest

from sitechecker import sitechecker


@pytest.mark.asyncio
async def test__given_normal_case__when_read_http__then_expected_result() -> None:
    async with aiohttp.ClientSession() as session:
        result = await sitechecker.read_http(session, "https://cnn.com")
        assert (result.http_status, result.regex_matches, result.error) == (200, None, None)
        assert result.total_time > timedelta()


@pytest.mark.asyncio
async def test__given_404_response__when_read_http__then_expected_result() -> None:
    async with aiohttp.ClientSession() as session:
        result = await sitechecker.read_http(session, "http://google.com/blah123987")
        assert (result.http_status, result.regex_matches, result.error) == (404, None, None)
        assert result.total_time > timedelta()


@pytest.mark.asyncio
async def test__given_not_existing_site__when_read_http__then_expected_result() -> None:
    async with aiohttp.ClientSession() as session:
        result = await sitechecker.read_http(session, "https://cnn.com123")
        assert (result.http_status, result.regex_matches) == (None, None)
        assert isinstance(result.error, aiohttp.client_exceptions.ClientConnectorError)
        assert result.total_time > timedelta()


# TODO: Add more error cases for read_http
