from saigon15.osm_rules import classify


def test_bus_stop_both_conventions():
    assert classify({"highway": "bus_stop"}) == "bus_stop"
    assert classify({"public_transport": "platform", "bus": "yes"}) == "bus_stop"


def test_health_group():
    for value in ("hospital", "clinic", "doctors"):
        assert classify({"amenity": value}) == "health"


def test_unknown_tags():
    assert classify({"amenity": "cafe"}) is None
    assert classify({}) is None
