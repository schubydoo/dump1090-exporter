"""Structural checks on the dump1090exporter metric specifications."""

import dump1090exporter.metrics


def test_specification_structure():
    """The Specs object must be a dict with 'aircraft' and 'stats' groups."""
    specs = dump1090exporter.metrics.Specs
    assert isinstance(specs, dict)

    assert "aircraft" in specs
    aircraft = specs["aircraft"]
    assert isinstance(aircraft, tuple)
    for entry in aircraft:
        assert isinstance(entry, tuple)
        assert len(entry) == 3

    assert "stats" in specs
    stats = specs["stats"]
    assert isinstance(stats, dict)
    for group, group_specs in stats.items():
        assert isinstance(group, str)
        for entry in group_specs:
            assert isinstance(entry, tuple)
            assert len(entry) == 3
