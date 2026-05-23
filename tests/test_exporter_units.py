"""Unit tests for `Dump1090Exporter` internals — fetch error paths,
process_aircraft edge cases, and process_stats edge cases."""

from __future__ import annotations

import json
import math
from pathlib import Path

import pytest
from aiohttp import web
from aioprometheus import REGISTRY

from dump1090exporter.exporter import (
    Dump1090Error,
    Dump1090Exporter,
    build_resources,
)

GOLDEN_DATA_DIR = Path(__file__).parent / "golden-data"


@pytest.fixture(autouse=True)
def _clear_registry():
    yield
    REGISTRY.clear()


@pytest.fixture
def exporter(tmp_path: Path) -> Dump1090Exporter:
    return Dump1090Exporter(resource_path=str(tmp_path))


def test_build_resources_constructs_paths():
    res = build_resources("http://example.com/data")
    assert res.base == "http://example.com/data"
    assert res.receiver == "http://example.com/data/receiver.json"
    assert res.stats == "http://example.com/data/stats.json"
    assert res.aircraft == "http://example.com/data/aircraft.json"


# ---------- _fetch ----------------------------------------------------------


async def test_fetch_file_path_returns_parsed_json(tmp_path: Path) -> None:
    payload = {"hello": "world", "n": 42}
    target = tmp_path / "x.json"
    target.write_text(json.dumps(payload), encoding="utf-8")

    exp = Dump1090Exporter(resource_path=str(tmp_path))
    result = await exp._fetch(str(target))
    assert result == payload


async def test_fetch_file_path_missing_raises_oserror(exporter: Dump1090Exporter) -> None:
    with pytest.raises(OSError):
        await exporter._fetch("/definitely/not/a/path/foo.json")


async def test_fetch_file_path_invalid_json_raises_valueerror(
    tmp_path: Path, exporter: Dump1090Exporter
) -> None:
    bad = tmp_path / "bad.json"
    bad.write_text("{not json", encoding="utf-8")
    with pytest.raises(ValueError):
        await exporter._fetch(str(bad))


async def test_fetch_http_non_200_raises_dump1090error() -> None:
    """A 500 from the dump1090 endpoint surfaces as Dump1090Error."""

    async def handler(_request: web.Request) -> web.Response:
        return web.Response(status=500, text="boom")

    app = web.Application()
    app.add_routes([web.get("/data/aircraft.json", handler)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "127.0.0.1")
    await site.start()
    try:
        exp = Dump1090Exporter(resource_path=site.name + "/data")
        with pytest.raises(Dump1090Error, match="Fetch failed 500"):
            await exp._fetch(exp.resources.aircraft)
    finally:
        await runner.cleanup()


async def test_fetch_http_client_error_raises_dump1090error() -> None:
    """A connection refused (no listener on port) wraps as Dump1090Error."""
    exp = Dump1090Exporter(resource_path="http://127.0.0.1:1/data", fetch_timeout=0.5)
    with pytest.raises(Dump1090Error):
        await exp._fetch(exp.resources.aircraft)


async def test_fetch_http_timeout_raises_dump1090error() -> None:
    """A handler that never replies trips the ClientTimeout."""

    async def slow_handler(_request: web.Request) -> web.Response:
        import asyncio

        await asyncio.sleep(5)
        return web.Response(text="never")

    app = web.Application()
    app.add_routes([web.get("/data/aircraft.json", slow_handler)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "127.0.0.1")
    await site.start()
    try:
        exp = Dump1090Exporter(resource_path=site.name + "/data", fetch_timeout=0.2)
        with pytest.raises(Dump1090Error):
            await exp._fetch(exp.resources.aircraft)
    finally:
        await runner.cleanup()


# ---------- process_aircraft -------------------------------------------------


def test_process_aircraft_with_no_origin_skips_range_math(
    exporter: Dump1090Exporter,
) -> None:
    """No origin → max_range stays 0 even with positioned aircraft."""
    exporter.origin = None
    exporter.process_aircraft(
        {
            "messages": 99,
            "aircraft": [
                {"seen": 1, "seen_pos": 1, "lat": -34.9, "lon": 138.6, "mlat": []},
            ],
        }
    )
    # Walk the gauge to confirm max_range was set to 0.
    max_range = exporter.metrics["aircraft"]["max_range"]
    assert max_range.get({"time_period": "latest"}) == 0.0


def test_process_aircraft_observed_threshold_drops_stale_entries(
    exporter: Dump1090Exporter,
) -> None:
    """Aircraft with `seen >= threshold` aren't counted as observed."""
    exporter.process_aircraft(
        {
            "messages": 1,
            "aircraft": [
                {"seen": 1, "seen_pos": None, "mlat": []},  # observed
                {"seen": 99, "seen_pos": None, "mlat": []},  # too stale
            ],
        }
    )
    observed = exporter.metrics["aircraft"]["observed"]
    assert observed.get({"time_period": "latest"}) == 1


def test_process_aircraft_with_origin_computes_max_range(tmp_path: Path) -> None:
    """End-to-end against the bundled golden-data aircraft.json — origin set,
    positioned aircraft, max_range should be > 0."""
    payload = json.loads((GOLDEN_DATA_DIR / "aircraft.json").read_text(encoding="utf-8"))
    exp = Dump1090Exporter(resource_path=str(tmp_path), origin=(-34.928500, 138.600700))
    exp.process_aircraft(payload)
    max_range = exp.metrics["aircraft"]["max_range"]
    assert max_range.get({"time_period": "latest"}) > 0.0


def test_process_aircraft_mlat_increment_with_origin(tmp_path: Path) -> None:
    exp = Dump1090Exporter(resource_path=str(tmp_path), origin=(0.0, 0.0))
    exp.process_aircraft(
        {
            "messages": 0,
            "aircraft": [
                {
                    "seen": 1,
                    "seen_pos": 1,
                    "lat": 1.0,
                    "lon": 1.0,
                    "mlat": {"lat": 1.0, "lon": 1.0},
                }
            ],
        }
    )
    assert exp.metrics["aircraft"]["observed_with_mlat"].get({"time_period": "latest"}) == 1


# ---------- process_stats ----------------------------------------------------


def test_process_stats_missing_time_period_logs_and_continues(
    exporter: Dump1090Exporter, caplog: pytest.LogCaptureFixture
) -> None:
    """Asking for a time period that isn't in the payload should log and
    proceed without raising."""
    import logging

    with caplog.at_level(logging.ERROR, logger="dump1090exporter.exporter"):
        exporter.process_stats({}, time_periods=("nope",))
    assert any("Problem extracting time period" in r.message for r in caplog.records)


def _full_stats_payload() -> dict:
    """A complete `last1min` payload covering every group dump1090 produces.

    Tests can deep-copy this and selectively delete keys to exercise the
    "missing metric" branch without tripping the strict group-required
    invariant in process_stats.
    """
    return {
        "last1min": {
            "messages": 100,
            "cpr": dict.fromkeys(
                (
                    "airborne",
                    "surface",
                    "filtered",
                    "global_bad",
                    "global_ok",
                    "global_range",
                    "global_skipped",
                    "global_speed",
                    "local_aircraft_relative",
                    "local_ok",
                    "local_range",
                    "local_receiver_relative",
                    "local_skipped",
                    "local_speed",
                ),
                0,
            ),
            "cpu": {"background": 0, "demod": 0, "reader": 0},
            "local": {
                "accepted": [0],
                "signal": 0,
                "peak_signal": 0,
                "noise": 0,
                "strong_signals": 0,
                "bad": 0,
                "modes": 0,
                "modeac": 0,
                "samples_dropped": 0,
                "samples_processed": 0,
                "unknown_icao": 0,
            },
            "tracks": {"all": 0, "single_message": 0},
            "remote": {
                "accepted": [0],
                "bad": 0,
                "modeac": 0,
                "modes": 0,
                "unknown_icao": 0,
            },
        }
    }


def test_process_stats_missing_signal_is_silent(
    exporter: Dump1090Exporter, caplog: pytest.LogCaptureFixture
) -> None:
    """`signal` and `peak_signal` go missing whenever there are no aircraft;
    the exporter should set NaN without logging a WARNING for those two."""
    import logging
    from copy import deepcopy

    payload = deepcopy(_full_stats_payload())
    del payload["last1min"]["local"]["signal"]
    del payload["last1min"]["local"]["peak_signal"]

    with caplog.at_level(logging.WARNING, logger="dump1090exporter.exporter"):
        exporter.process_stats(payload, time_periods=("last1min",))

    warnings = [r.message for r in caplog.records if r.levelno == logging.WARNING]
    assert not any("signal" in m for m in warnings)
    assert not any("peak_signal" in m for m in warnings)

    signal = exporter.metrics["stats"]["local"]["signal"]
    assert math.isnan(signal.get({"time_period": "last1min"}))


def test_process_stats_missing_non_signal_metric_warns_and_sets_nan(
    exporter: Dump1090Exporter, caplog: pytest.LogCaptureFixture
) -> None:
    """A missing metric that isn't signal/peak_signal logs WARNING and stores NaN."""
    import logging
    from copy import deepcopy

    payload = deepcopy(_full_stats_payload())
    del payload["last1min"]["cpu"]["background"]

    with caplog.at_level(logging.WARNING, logger="dump1090exporter.exporter"):
        exporter.process_stats(payload, time_periods=("last1min",))

    warnings = [r.message for r in caplog.records if r.levelno == logging.WARNING]
    assert any("background" in m for m in warnings)
    background = exporter.metrics["stats"]["cpu"]["background"]
    assert math.isnan(background.get({"time_period": "last1min"}))


def test_process_stats_accepted_list_value_is_unwrapped(
    exporter: Dump1090Exporter,
) -> None:
    """The `accepted` value comes as a list; the exporter must unwrap [0]."""
    payload = {
        "last1min": {
            "messages": 100,
            "cpr": dict.fromkeys(
                (
                    "airborne",
                    "surface",
                    "filtered",
                    "global_bad",
                    "global_ok",
                    "global_range",
                    "global_skipped",
                    "global_speed",
                    "local_aircraft_relative",
                    "local_ok",
                    "local_range",
                    "local_receiver_relative",
                    "local_skipped",
                    "local_speed",
                ),
                0,
            ),
            "cpu": {"background": 0, "demod": 0, "reader": 0},
            "local": {
                "accepted": [777, 1, 2],  # ← list form
                "noise": 0,
                "strong_signals": 0,
                "bad": 0,
                "modes": 0,
                "modeac": 0,
                "samples_dropped": 0,
                "samples_processed": 0,
                "unknown_icao": 0,
            },
            "tracks": {"all": 0, "single_message": 0},
            "remote": {
                "accepted": [0, 0],
                "bad": 0,
                "modeac": 0,
                "modes": 0,
                "unknown_icao": 0,
            },
        }
    }
    exporter.process_stats(payload, time_periods=("last1min",))
    accepted = exporter.metrics["stats"]["local"]["accepted"]
    assert accepted.get({"time_period": "last1min"}) == 777
