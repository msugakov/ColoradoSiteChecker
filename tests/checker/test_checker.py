import pytest

from sitechecker import sitechecker


@pytest.mark.asyncio
async def test_read_http() -> None:
    print("Hello world!")
    await sitechecker.read_http("https://cnn.com")
    assert 1 == 1
