#!/usr/bin/env python

import asyncio
import signal

import aiohttp
from apscheduler.events import EVENT_JOB_ERROR
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from logzero import logger

POLLING_SCHEDULE = {
    "trigger": "interval",
    "seconds": 3,
}


async def tick() -> None:
    await read_http("https://aiven.io/about")


async def read_http(url: str) -> None:
    # The manual says we should not close session after every request because
    # there's a connection pool.
    # See https://docs.aiohttp.org/en/stable/client_quickstart.html#make-a-request
    # However we'd like to measure "cold" request time including DNS resolution (TODO: verify)
    # and establishing connection.
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print(response.status)
            print()


def setup_scheduler_application():
    def shutdown_application():
        logger.debug("Shutting down job scheduler")
        scheduler.shutdown(wait=True)
        logger.debug("Stopping event loop")
        asyncio.get_event_loop().stop()
        logger.debug("The application should shut down now")

    def on_job_error(event):
        logger.error(
            "Error when executing scheduled job. Shutting down application...",
            exc_info=event.exception,
        )
        shutdown_application()

    def on_signal(signal):
        logger.info(f"Received signal {signal}. Shutting down application...")
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
    print("done")


if __name__ == "__main__":
    main()
