"""Unit tests for the geometry helpers in `dump1090exporter.exporter`."""

from __future__ import annotations

import math

import pytest

from dump1090exporter.exporter import (
    Position,
    haversine_distance,
    relative_angle,
    relative_direction,
)


class TestRelativeAngle:
    """`relative_angle` returns the bearing of pos2 from pos1 in [0, 360)."""

    def test_due_north(self):
        # pos2 directly north of pos1 → 0°
        assert relative_angle(Position(0.0, 0.0), Position(1.0, 0.0)) == 0.0

    def test_due_south(self):
        # pos2 directly south of pos1 → 180°
        assert relative_angle(Position(0.0, 0.0), Position(-1.0, 0.0)) == 180.0

    def test_due_east_same_latitude(self):
        # Same-latitude branch (lat2 == lat1, lon2 > lon1) → 90°
        assert relative_angle(Position(10.0, 0.0), Position(10.0, 5.0)) == 90.0

    def test_due_west_same_latitude(self):
        # Same-latitude branch (lat2 == lat1, lon2 < lon1) → 270°
        assert relative_angle(Position(10.0, 0.0), Position(10.0, -5.0)) == 270.0

    def test_quadrant_ne(self):
        # Northeast: 0 < angle < 90
        angle = relative_angle(Position(0.0, 0.0), Position(1.0, 1.0))
        assert 0.0 < angle < 90.0

    def test_quadrant_se(self):
        # Southeast: 90 < angle < 180
        angle = relative_angle(Position(0.0, 0.0), Position(-1.0, 1.0))
        assert 90.0 < angle < 180.0

    def test_quadrant_sw(self):
        # Southwest: 180 < angle < 270
        angle = relative_angle(Position(0.0, 0.0), Position(-1.0, -1.0))
        assert 180.0 < angle < 270.0

    def test_quadrant_nw(self):
        # Northwest: 270 < angle < 360
        angle = relative_angle(Position(0.0, 0.0), Position(1.0, -1.0))
        assert 270.0 < angle < 360.0


class TestRelativeDirection:
    """Cardinal direction lookup from an angle."""

    @pytest.mark.parametrize(
        ("angle", "expected"),
        [
            (0.0, "N"),
            (22.5, "NE"),
            (45.0, "NE"),
            (67.5, "E"),
            (90.0, "E"),
            (135.0, "SE"),
            (180.0, "S"),
            (225.0, "SW"),
            (270.0, "W"),
            (315.0, "NW"),
            (359.999, "N"),  # wraps via 16-entry lookup
        ],
    )
    def test_known_angles(self, angle: float, expected: str):
        assert relative_direction(angle) == expected


class TestHaversineDistance:
    """Great-circle distance between two points on a sphere."""

    def test_same_point_is_zero(self):
        assert haversine_distance(Position(0.0, 0.0), Position(0.0, 0.0)) == 0.0

    def test_antipodes(self):
        # Antipodal points on Earth ≈ π * R = ~20015 km (in metres).
        dist = haversine_distance(Position(0.0, 0.0), Position(0.0, 180.0))
        expected = math.pi * 6371.0e3
        assert math.isclose(dist, expected, rel_tol=1e-6)

    def test_one_degree_latitude_step(self):
        # 1° of latitude along a meridian ≈ 111.195 km (πR/180).
        dist = haversine_distance(Position(0.0, 0.0), Position(1.0, 0.0))
        assert math.isclose(dist, math.pi * 6371.0e3 / 180.0, rel_tol=1e-9)

    def test_known_long_distance(self):
        # Adelaide (the golden-data origin) → Sydney is roughly 1163 km.
        adelaide = Position(-34.9285, 138.6007)
        sydney = Position(-33.8688, 151.2093)
        dist_km = haversine_distance(adelaide, sydney) / 1000.0
        # Loose bound — verifies order of magnitude + sign.
        assert 1100.0 < dist_km < 1230.0

    def test_custom_radius(self):
        # Custom sphere radius scales the result linearly.
        a = Position(0.0, 0.0)
        b = Position(1.0, 0.0)
        d_earth = haversine_distance(a, b)
        d_half = haversine_distance(a, b, radius=6371.0e3 / 2)
        assert math.isclose(d_half, d_earth / 2, rel_tol=1e-12)
