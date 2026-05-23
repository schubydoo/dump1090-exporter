"""Collect data from a dump1090 service and expose it as Prometheus metrics."""

from __future__ import annotations

import asyncio
import contextlib
import datetime
import json
import logging
import math
from collections.abc import Sequence
from math import asin, atan, cos, degrees, radians, sin, sqrt
from pathlib import Path
from typing import Any, NamedTuple

import aiohttp
from aioprometheus import Gauge
from aioprometheus.service import Service

from .metrics import Specs

PositionType = tuple[float, float]
MetricSpecItemType = tuple[str, str, str]
MetricsSpecGroupType = Sequence[MetricSpecItemType]

logger = logging.getLogger(__name__)


class Dump1090Error(Exception):
    """Raised when a dump1090 resource cannot be fetched or parsed."""


AircraftKeys = (
    "altitude",
    "category",
    "flight",
    "hex",
    "lat",
    "lon",
    "messages",
    "mlat",
    "nucp",
    "rssi",
    "seen",
    "seen_pos",
    "speed",
    "squalk",
    "tisb",
    "track",
    "vert_rate",
    "rel_angle",
    "rel_direction",
)


class Dump1090Resources(NamedTuple):
    """Paths/URLs for the dump1090 JSON resources scraped by the exporter."""

    base: str
    receiver: str
    stats: str
    aircraft: str


class Position(NamedTuple):
    """A (lat, lon) pair in decimal degrees."""

    latitude: float
    longitude: float


def build_resources(base: str) -> Dump1090Resources:
    """Return a named tuple containing dump1090 resource paths."""
    return Dump1090Resources(
        base=base,
        receiver=f"{base}/receiver.json",
        stats=f"{base}/stats.json",
        aircraft=f"{base}/aircraft.json",
    )


def relative_angle(pos1: Position, pos2: Position) -> float:
    """Calculate the bearing of ``pos2`` relative to ``pos1`` in degrees."""
    lat1, lon1 = pos1
    lat2, lon2 = pos2

    # Same latitude: aircraft is due east or due west.
    if lat2 == lat1:
        return 90.0 if lon2 > lon1 else 270.0

    deg = degrees(atan((lon2 - lon1) / (lat2 - lat1)))
    # Convert atan result into 0-360 range
    if lat2 > lat1:
        return (360 + deg) % 360
    return 180 + deg


# lookup table for directions - each step is 22.5 degrees
direction_lut = (
    "N",
    "NE",
    "NE",
    "E",
    "E",
    "SE",
    "SE",
    "S",
    "S",
    "SW",
    "SW",
    "W",
    "W",
    "NW",
    "NW",
    "N",
)


def relative_direction(angle: float) -> str:
    """Convert a relative angle in degrees into a cardinal direction."""
    return direction_lut[int(angle / 22.5)]


def haversine_distance(pos1: Position, pos2: Position, radius: float = 6371.0e3) -> float:
    """Great-circle distance between two ``Position`` points on a sphere.

    Defaults to the Earth's radius (in meters).
    """
    lat1, lon1, lat2, lon2 = (radians(x) for x in (*pos1, *pos2))

    hav = sin((lat2 - lat1) / 2.0) ** 2 + cos(lat1) * cos(lat2) * sin((lon2 - lon1) / 2.0) ** 2
    return 2 * radius * asin(sqrt(hav))


def create_gauge_metric(label: str, doc: str, prefix: str = "") -> Gauge:
    """Create a Gauge metric with the given label, help text, and optional prefix."""
    return Gauge(f"{prefix}{label}", doc)


class Dump1090Exporter:
    """Fetch, parse, and export dump1090 metrics to Prometheus."""

    def __init__(
        self,
        resource_path: str,
        host: str = "",
        port: int = 9105,
        aircraft_interval: int = 10,
        stats_interval: int = 60,
        receiver_interval: int = 10,
        receiver_interval_origin_ok: int = 300,
        time_periods: Sequence[str] = ("last1min",),
        origin: PositionType | None = None,
        fetch_timeout: float = 2.0,
    ) -> None:
        self.resources = build_resources(resource_path)
        self.host = host
        self.port = port
        self.prefix = "dump1090_"
        self.receiver_interval = datetime.timedelta(seconds=receiver_interval)
        self.receiver_interval_origin_ok = datetime.timedelta(seconds=receiver_interval_origin_ok)
        self.aircraft_interval = datetime.timedelta(seconds=aircraft_interval)
        self.stats_interval = datetime.timedelta(seconds=stats_interval)
        self.stats_time_periods = time_periods
        self.origin: Position | None = Position(*origin) if origin else None
        self.fetch_timeout = fetch_timeout
        self.svr = Service()
        self.receiver_task: asyncio.Task[None] | None = None
        self.stats_task: asyncio.Task[None] | None = None
        self.aircraft_task: asyncio.Task[None] | None = None
        self.metrics: dict[str, Any] = {"aircraft": {}, "stats": {}}
        self.initialise_metrics()
        logger.info("Monitoring dump1090 resources at: %s", self.resources.base)
        logger.info(
            "Refresh rates: aircraft=%s, statistics=%s",
            self.aircraft_interval,
            self.stats_interval,
        )
        logger.info("Origin: %s", self.origin)

    async def start(self) -> None:
        """Start the metrics server and the background scraper tasks."""
        await self.svr.start(addr=self.host, port=self.port)
        logger.info("serving dump1090 prometheus metrics on: %s", self.svr.metrics_url)

        self.receiver_task = asyncio.create_task(self.updater_receiver())
        self.stats_task = asyncio.create_task(self.updater_stats())
        self.aircraft_task = asyncio.create_task(self.updater_aircraft())

    async def stop(self) -> None:
        """Cancel the background tasks and stop the metrics server."""
        for attr in ("receiver_task", "stats_task", "aircraft_task"):
            task: asyncio.Task[None] | None = getattr(self, attr)
            if task is None:
                continue
            task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await task
            setattr(self, attr, None)

        await self.svr.stop()

    def initialise_metrics(self) -> None:
        """Create the Prometheus gauges for aircraft and stats groups."""
        # aircraft
        aircraft_metrics: dict[str, Gauge] = self.metrics["aircraft"]
        for name, label, doc in Specs["aircraft"]:
            aircraft_metrics[name] = create_gauge_metric(label, doc, prefix=self.prefix)

        # statistics
        for group, metrics_specs in Specs["stats"].items():
            group_metrics: dict[str, Gauge] = self.metrics["stats"].setdefault(group, {})
            for name, label, doc in metrics_specs:
                group_metrics[name] = create_gauge_metric(label, doc, prefix=self.prefix)

    async def _fetch(self, resource: str) -> dict[Any, Any]:
        """Fetch JSON data from an HTTP URL or local file path."""
        logger.debug("fetching %s", resource)
        if resource.startswith(("http://", "https://")):
            timeout = aiohttp.ClientTimeout(total=self.fetch_timeout)
            try:
                async with (
                    aiohttp.ClientSession(timeout=timeout) as session,
                    session.get(resource) as resp,
                ):
                    if resp.status != 200:
                        raise Dump1090Error(f"Fetch failed {resp.status}: {resource}")
                    return await resp.json()
            except TimeoutError as exc:
                raise Dump1090Error(f"Request timed out to {resource}") from exc
            except aiohttp.ClientError as exc:
                raise Dump1090Error(f"Client error {exc}, {resource}") from exc

        path = Path(resource)
        return json.loads(path.read_text(encoding="utf-8"))

    async def updater_receiver(self) -> None:
        """Periodically refresh the receiver origin from ``receiver.json``."""
        while True:
            start = datetime.datetime.now()
            try:
                receiver = await self._fetch(self.resources.receiver)
                if receiver and "lat" in receiver and "lon" in receiver:
                    self.origin = Position(receiver["lat"], receiver["lon"])
                    logger.info(
                        "Origin successfully extracted from receiver data: %s",
                        self.origin,
                    )
            except Dump1090Error as exc:
                logger.error("Error fetching dump1090 receiver data: %s", exc)
            except (OSError, ValueError) as exc:
                logger.error("Error parsing dump1090 receiver data: %s", exc)

            end = datetime.datetime.now()
            interval = self.receiver_interval_origin_ok if self.origin else self.receiver_interval
            wait_seconds = max(0.0, (start + interval - end).total_seconds())
            await asyncio.sleep(wait_seconds)

    async def updater_stats(self) -> None:
        """Periodically refresh stats metrics from ``stats.json``."""
        while True:
            start = datetime.datetime.now()
            try:
                stats = await self._fetch(self.resources.stats)
                self.process_stats(stats, time_periods=self.stats_time_periods)
            except Dump1090Error as exc:
                logger.error("Error fetching dump1090 stats data: %s", exc)
            except (OSError, ValueError) as exc:
                logger.error("Error parsing dump1090 stats data: %s", exc)

            end = datetime.datetime.now()
            wait_seconds = max(0.0, (start + self.stats_interval - end).total_seconds())
            await asyncio.sleep(wait_seconds)

    async def updater_aircraft(self) -> None:
        """Periodically refresh aircraft metrics from ``aircraft.json``."""
        while True:
            start = datetime.datetime.now()
            try:
                aircraft = await self._fetch(self.resources.aircraft)
                self.process_aircraft(aircraft)
            except Dump1090Error as exc:
                logger.error("Error fetching dump1090 aircraft data: %s", exc)
            except (OSError, ValueError) as exc:
                logger.error("Error parsing dump1090 aircraft data: %s", exc)

            end = datetime.datetime.now()
            wait_seconds = max(0.0, (start + self.aircraft_interval - end).total_seconds())
            await asyncio.sleep(wait_seconds)

    def process_stats(self, stats: dict, time_periods: Sequence[str] = ("last1min",)) -> None:
        """Update stats gauges from a dump1090 stats payload."""
        metrics: dict[str, dict[str, Gauge]] = self.metrics["stats"]

        for time_period in time_periods:
            try:
                tp_stats = stats[time_period]
            except KeyError:
                logger.exception("Problem extracting time period: %s", time_period)
                continue

            labels = {"time_period": time_period}

            for key, gauge in metrics.items():
                d = tp_stats[key] if key else tp_stats
                for name, metric in gauge.items():
                    try:
                        value = d[name]
                        # 'accepted' values are in a list
                        if isinstance(value, list):
                            value = value[0]
                    except KeyError:
                        # 'signal' and 'peak_signal' are not present if
                        # there are no aircraft.
                        if name not in ("peak_signal", "signal"):
                            key_str = f" {key} " if key else " "
                            logger.warning(
                                "Problem extracting%sitem '%s' from: %s",
                                key_str,
                                name,
                                d,
                            )
                        value = math.nan
                    metric.set(labels, value)

    def process_aircraft(self, aircraft: dict, threshold: int = 15) -> None:
        """Update aircraft gauges from a dump1090 aircraft payload."""
        # Ensure aircraft dict always contains all keys, as optional
        # items are not always present.
        for entry in aircraft["aircraft"]:
            for key in AircraftKeys:
                entry.setdefault(key, None)

        messages = aircraft["messages"]

        # 'seen' shows how long ago (in seconds before "now") a message
        # was last received from an aircraft.
        # 'seen_pos' shows how long ago (in seconds before "now") the
        # position was last updated.
        aircraft_observed = 0
        aircraft_with_pos = 0
        aircraft_with_mlat = 0
        aircraft_max_range = 0.0
        aircraft_direction = {
            "N": 0,
            "NE": 0,
            "E": 0,
            "SE": 0,
            "S": 0,
            "SW": 0,
            "W": 0,
            "NW": 0,
        }
        aircraft_direction_max_range = {
            "N": 0.0,
            "NE": 0.0,
            "E": 0.0,
            "SE": 0.0,
            "S": 0.0,
            "SW": 0.0,
            "W": 0.0,
            "NW": 0.0,
        }
        # Filter aircraft to those seen within the last n seconds to minimise
        # contributions from aged observations.
        for a in aircraft["aircraft"]:
            if a["seen"] < threshold:
                aircraft_observed += 1
            if a["seen_pos"] and a["seen_pos"] < threshold:
                aircraft_with_pos += 1
                if self.origin:
                    distance = haversine_distance(self.origin, Position(a["lat"], a["lon"]))
                    aircraft_max_range = max(aircraft_max_range, distance)

                    a["rel_angle"] = relative_angle(self.origin, Position(a["lat"], a["lon"]))
                    a["rel_direction"] = relative_direction(a["rel_angle"])
                    aircraft_direction[a["rel_direction"]] += 1
                    if distance > aircraft_direction_max_range[a["rel_direction"]]:
                        aircraft_direction_max_range[a["rel_direction"]] = distance

                if a["mlat"] and "lat" in a["mlat"]:
                    aircraft_with_mlat += 1

        labels = {"time_period": "latest"}
        d = self.metrics["aircraft"]
        d["observed"].set(labels, aircraft_observed)
        d["observed_with_pos"].set(labels, aircraft_with_pos)
        d["observed_with_mlat"].set(labels, aircraft_with_mlat)
        d["max_range"].set(labels, aircraft_max_range)
        d["messages_total"].set(labels, messages)

        for direction, value in aircraft_direction.items():
            dir_labels = {"time_period": "latest", "direction": direction}
            d["observed_with_direction"].set(dir_labels, value)
            d["max_range_by_direction"].set(dir_labels, aircraft_direction_max_range[direction])

        logger.debug(
            "aircraft: observed=%s, with_pos=%s, with_mlat=%s, max_range=%s, messages=%s",
            aircraft_observed,
            aircraft_with_pos,
            aircraft_with_mlat,
            aircraft_max_range,
            messages,
        )
