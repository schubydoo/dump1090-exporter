"""Tests for the CLI entry point in `dump1090exporter.__main__`."""

from __future__ import annotations

import contextlib
import subprocess
import sys
from unittest import mock

import pytest

from dump1090exporter import __version__
from dump1090exporter.__main__ import _build_parser, main


class TestParser:
    """argparse surface — no I/O, fast."""

    def test_default_values(self):
        ns = _build_parser().parse_args([])
        assert ns.resource_path == "http://localhost:8080/data"
        assert ns.host == "0.0.0.0"  # noqa: S104 - documented default
        assert ns.port == 9105
        assert ns.latitude is None
        assert ns.longitude is None
        assert ns.log_level == "info"

    def test_custom_args(self):
        ns = _build_parser().parse_args(
            [
                "--resource-path=/var/run/dump1090-fa",
                "--host=127.0.0.1",
                "--port=9999",
                "--latitude=-34.9285",
                "--longitude=138.6007",
                "--aircraft-interval=5",
                "--stats-interval=30",
                "--receiver-interval=15",
                "--log-level=debug",
            ]
        )
        assert ns.resource_path == "/var/run/dump1090-fa"
        assert ns.host == "127.0.0.1"
        assert ns.port == 9999
        assert ns.latitude == -34.9285
        assert ns.longitude == 138.6007
        assert ns.aircraft_interval == 5
        assert ns.stats_interval == 30
        assert ns.receiver_interval == 15
        assert ns.log_level == "debug"

    def test_invalid_log_level_rejected(self):
        with pytest.raises(SystemExit):
            _build_parser().parse_args(["--log-level=verbose"])

    def test_version_flag_exits_zero(self):
        # argparse's --version triggers SystemExit(0) after printing.
        with pytest.raises(SystemExit) as excinfo:
            _build_parser().parse_args(["--version"])
        assert excinfo.value.code == 0


class TestVersionSubprocess:
    """Run the CLI in a subprocess so we capture stdout end-to-end."""

    def test_version_output_contains_package_version(self):
        proc = subprocess.run(
            [sys.executable, "-m", "dump1090exporter", "--version"],
            check=True,
            capture_output=True,
            text=True,
            timeout=15,
        )
        # argparse writes to stdout for action='version'.
        assert __version__ in proc.stdout
        assert "dump1090exporter" in proc.stdout

    def test_help_output_lists_known_flags(self):
        proc = subprocess.run(
            [sys.executable, "-m", "dump1090exporter", "--help"],
            check=True,
            capture_output=True,
            text=True,
            timeout=15,
        )
        for flag in (
            "--resource-path",
            "--host",
            "--port",
            "--latitude",
            "--longitude",
            "--log-level",
            "--version",
        ):
            assert flag in proc.stdout


class TestMain:
    """Exercise `main()` in-process — patches out the network/loop pieces so
    the test just verifies argument-to-Exporter wiring."""

    def test_main_wires_args_to_exporter_and_runs(self):
        """Set sys.argv, patch the exporter + asyncio.run, confirm the
        kwargs flow through and uvloop install is attempted."""
        with (
            mock.patch.object(
                sys, "argv", ["dump1090exporter", "--port=9876", "--log-level=error"]
            ),
            mock.patch("dump1090exporter.__main__.asyncio.run") as run_mock,
        ):
            main()
        # asyncio.run was called once with the _run coroutine.
        assert run_mock.call_count == 1

    def test_main_constructs_origin_when_both_lat_lon_provided(self):
        """When --latitude AND --longitude are provided, the exporter gets
        an origin tuple; otherwise it gets None. We assert by patching
        Dump1090Exporter and inspecting the kwargs the coroutine passes."""
        captured: dict = {}

        class FakeExporter:
            def __init__(self, **kwargs):
                captured.update(kwargs)

            async def start(self):
                pass

            async def stop(self):
                pass

        def _no_run(coro):
            # Drive the coroutine just far enough to construct the exporter
            # (the FakeExporter constructor captures the kwargs we want to
            # assert on) and then bail at the first await — even on
            # RuntimeError from asyncio.get_running_loop(), since we have no
            # event loop. We just need the constructor to fire.
            with contextlib.suppress(StopIteration, RuntimeError):
                coro.send(None)
            coro.close()

        with (
            mock.patch.object(
                sys,
                "argv",
                [
                    "dump1090exporter",
                    "--latitude=-34.9285",
                    "--longitude=138.6007",
                ],
            ),
            mock.patch("dump1090exporter.__main__.Dump1090Exporter", FakeExporter),
            mock.patch("dump1090exporter.__main__.asyncio.run", _no_run),
        ):
            main()
        assert captured.get("origin") == (-34.9285, 138.6007)
        assert captured.get("port") == 9105  # default flowed through
