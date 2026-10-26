import pandas as pd

from saigon15.dedup import merge_duplicates, normalize_name

BASE_LAT, BASE_LON = 10.7725, 106.6980


def make(rows):
    """rows: danh sach (osm_type, osm_id, category, name, lat_offset)."""
    return pd.DataFrame(
        [(t, i, c, n, BASE_LAT + off, BASE_LON) for t, i, c, n, off in rows],
        columns=["osm_type", "osm_id", "category", "name", "lat", "lon"],
    )


def check_totals(stats):
    assert stats["before"] - stats["after"] == sum(stats["merged"].values())


def test_removes_accents_and_case():
    assert normalize_name("Chợ Bến Thành") == "cho ben thanh"


def test_collapses_spaces():
    assert normalize_name("  cho   BEN thanh ") == "cho ben thanh"


def test_d_with_stroke():
    assert normalize_name("Đại học Khoa Học Tự Nhiên") == "dai hoc khoa hoc tu nhien"


def test_empty_values_return_none():
    for value in (None, "", "   ", float("nan")):
        assert normalize_name(value) is None


def test_near_duplicates_are_merged_and_node_is_kept():
    df = make(
        [
            ("way", 2, "school", "Truong A", 0.0),
            ("node", 9, "school", "truong a", 0.00018),
        ]
    )
    merged, stats = merge_duplicates(df)
    assert len(merged) == 1
    assert merged.iloc[0]["osm_type"] == "node"
    assert stats["merged"]["school"] == 1
    check_totals(stats)


def test_far_points_are_kept():
    df = make([("node", 1, "market", "Cho A", 0.0), ("node", 2, "market", "Cho A", 0.0018)])
    merged, stats = merge_duplicates(df)
    assert len(merged) == 2
    assert stats["merged"]["market"] == 0
    check_totals(stats)


def test_different_category_is_kept():
    df = make([("node", 1, "school", "A", 0.0), ("node", 2, "health", "A", 0.0)])
    merged, _ = merge_duplicates(df)
    assert len(merged) == 2


def test_chain_of_points_forms_one_cluster():
    df = make(
        [
            ("node", 1, "bus_stop", "Ben B", 0.0),
            ("node", 2, "bus_stop", "Ben B", 0.00036),
            ("node", 3, "bus_stop", "Ben B", 0.00072),
        ]
    )
    merged, stats = merge_duplicates(df)
    assert len(merged) == 1
    assert stats["merged"]["bus_stop"] == 2
    check_totals(stats)


def test_unnamed_points_are_never_merged():
    df = make([("node", 1, "park", None, 0.0), ("node", 2, "park", None, 0.0)])
    merged, stats = merge_duplicates(df)
    assert len(merged) == 2
    assert stats["unnamed"] == 2


def test_names_differing_only_by_accent_are_merged():
    df = make([("node", 1, "market", "Chợ A", 0.0), ("node", 2, "market", "cho a", 0.00009)])
    merged, _ = merge_duplicates(df)
    assert len(merged) == 1


def test_threshold_parameter_is_respected():
    df = make([("node", 1, "school", "A", 0.0), ("node", 2, "school", "A", 0.00018)])
    assert len(merge_duplicates(df, threshold_m=10)[0]) == 2
    assert len(merge_duplicates(df, threshold_m=50)[0]) == 1
