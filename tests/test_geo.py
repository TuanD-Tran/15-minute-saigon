from saigon15.geo import haversine_m


def test_zero_distance():
    assert haversine_m(10.77, 106.69, 10.77, 106.69) == 0


def test_one_millidegree_of_latitude_is_about_111_m():
    assert abs(haversine_m(10.0, 106.0, 10.001, 106.0) - 111.2) < 0.5
