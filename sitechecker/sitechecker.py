#!/usr/bin/env python

import asyncio
import signal
import types
from typing import NamedTuple, Optional

from datetime import timedelta
import time
import aiohttp
from apscheduler.events import EVENT_JOB_ERROR
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from logzero import logger

POLLING_SCHEDULE = types.MappingProxyType({"trigger": "interval", "seconds": 3})


class HttpReadResult(NamedTuple):
    """Results of site check."""

    http_status: Optional[int]
    regex_matches: Optional[bool]
    error: Optional[Exception]

    # Total time in seconds for servicing request.
    # It includes DNS resolution, TCP connection establising, TLS/SSL handshake, sending the
    # request, server processing and receiving the response.
    # Note that we deviate from the problem definition which is asking to measure only "HTTP
    # response time".
    # Firstly,  with aiohttp it is just hard to measure only the time between request was submitted
    # and response came back.
    # Secondly, most service frameworks can easily capture the metric of "HTTP response time" but
    # they can't get a latency metric as the client sees it. Total time metric could be at least as
    # useful as HTTP response time.
    total_time: timedelta


async def tick() -> None:
    # The manual says we should not close session after every request because
    # there's a connection pool.
    # See https://docs.aiohttp.org/en/stable/client_quickstart.html#make-a-request
    # However we'd like to measure "cold" request time including DNS resolution (TODO: verify) and
    # establishing connection. Assumption: all monitored URLs are different sites and connection
    # caching does not improve request latency for requests within this session.
    async with aiohttp.ClientSession() as session:
        await read_http(session, "https://aiven.io/about")


async def read_http(session: aiohttp.ClientSession, url: str) -> HttpReadResult:
    logger.debug(f"Checking {url}")
    http_status = None
    regex_matches = None
    error = None
    start_counter = time.perf_counter()
    try:
        async with session.get(url) as response:
            end_counter = time.perf_counter()
            logger.info(response.status)  # TODO: move me
            http_status = response.status
    except Exception as err:
        end_counter = time.perf_counter()
        logger.warning(f"Problem communicating with {url}", exc_info=err)
        error = err

    result = HttpReadResult(
        http_status=http_status,
        regex_matches=None,
        error=error,
        total_time=timedelta(seconds=end_counter - start_counter),
    )
    logger.info(f"{url}: {result}")
    return result


def setup_scheduler_application():  # noqa: WPS213
    def shutdown_application():  # noqa:  WPS430
        logger.debug("Shutting down job scheduler")
        scheduler.shutdown(wait=True)
        logger.debug("Stopping event loop")
        asyncio.get_event_loop().stop()
        logger.debug("The application should shut down now")

    def on_job_error(event):  # noqa:  WPS430
        logger.error(
            "Error when executing scheduled job. Shutting down application...",
            exc_info=event.exception,
        )
        shutdown_application()

    def on_signal(signal_code):  # noqa:  WPS430
        logger.info(f"Received signal {signal_code}. Shutting down application...")
        shutdown_application()

    scheduler = AsyncIOScheduler(logger=logger)
    scheduler.add_listener(on_job_error, mask=EVENT_JOB_ERROR)

    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, on_signal, "SIGINT")
    loop.add_signal_handler(signal.SIGTERM, on_signal, "SIGTERM")

    return scheduler


def main():
    scheduler = setup_scheduler_application()

    scheduler.add_job(tick, **POLLING_SCHEDULE)
    scheduler.start()
    asyncio.get_event_loop().run_forever()
    # TODO: catch KeyboardInterrupt and SystemExit
    logger.info("done")


if __name__ == "__main__":
    main()
