"""Integration tests for the dump1090exporter against an emulated dump1090."""

from __future__ import annotations

import asyncio
import logging
from pathlib import Path

import pytest
from aiohttp import ClientSession, web
from aioprometheus import REGISTRY

import dump1090exporter.metrics
from dump1090exporter import Dump1090Exporter

GOLDEN_DATA_DIR = Path(__file__).parent / "golden-data"
AIRCRAFT_DATA_FILE = GOLDEN_DATA_DIR / "aircraft.json"
STATS_DATA_FILE = GOLDEN_DATA_DIR / "stats.json"
RECEIVER_DATA_FILE = GOLDEN_DATA_DIR / "receiver.json"
TEST_ORIGIN = (-34.928500, 138.600700)  # (lat, lon)


class Dump1090ServiceEmulator:
    """Tiny HTTP server that serves the golden dump1090 JSON files."""

    def __init__(self) -> None:
        self._runner: web.AppRunner | None = None
        self.url: str | None = None
        self.paths = {
            "/aircraft.json": AIRCRAFT_DATA_FILE,
            "/stats.json": STATS_DATA_FILE,
            "/receiver.json": RECEIVER_DATA_FILE,
        }

    async def handle_request(self, request: web.Request) -> web.Response:
        if request.path not in self.paths:
            raise RuntimeError(f"Unhandled path: {request.path}")
        data_file = self.paths[request.path]
        content = data_file.read_text(encoding="utf-8")
        return web.Response(status=200, body=content, content_type="application/json")

    async def start(self, addr: str = "127.0.0.1", port: int | None = None) -> None:
        app = web.Application()
        app.add_routes([web.get(request_path, self.handle_request) for request_path in self.paths])
        self._runner = web.AppRunner(app)
        await self._runner.setup()
        site = web.TCPSite(self._runner, addr, port)
        await site.start()
        self.url = site.name

    async def stop(self) -> None:
        assert self._runner is not None
        await self._runner.cleanup()


@pytest.fixture(autouse=True)
def _clear_registry():
    yield
    REGISTRY.clear()


async def test_exporter(caplog: pytest.LogCaptureFixture) -> None:
    """End-to-end: start the exporter against the emulator and scrape it."""
    ds = Dump1090ServiceEmulator()
    try:
        await ds.start()

        de = Dump1090Exporter(resource_path=ds.url, host="127.0.0.1", origin=TEST_ORIGIN)
        await de.start()
        await asyncio.sleep(0.3)

        async with (
            ClientSession() as session,
            session.get(de.svr.metrics_url, timeout=0.3) as resp,
        ):
            assert resp.status == 200, await resp.text()
            data = await resp.text()

        specs = dump1090exporter.metrics.Specs
        for _attr, label, _doc in specs["aircraft"]:
            assert f"{de.prefix}{label}{{" in data
        for _group_name, group_metrics in specs["stats"].items():
            for _attr, label, _doc in group_metrics:
                assert f"{de.prefix}{label}{{" in data

        await de.stop()

        # Calling stop again must be a no-op (and aioprometheus logs a warning).
        with caplog.at_level(logging.WARNING, logger="aioprometheus.service"):
            await de.stop()
        assert any("already stopped" in record.message for record in caplog.records)
    finally:
        await ds.stop()
