import json
from datetime import date
from pathlib import Path

import h3
import pandas as pd

from saigon15.config import H3_RES
from saigon15.dedup import merge_duplicates
from saigon15.osm_rules import classify


def load_pois(path: str = "data/raw/pois.json") -> pd.DataFrame:
    elements = json.loads(Path(path).read_text(encoding="utf-8"))["elements"]
    rows = []

    for el in elements:
        category = classify(el.get("tags", {}))
        if category is None:
            continue
        point = el if "lat" in el else el.get("center")
        if not point:
            continue
        rows.append(
            {
                "osm_type": el["type"],
                "osm_id": el["id"],
                "category": category,
                "name": el["tags"].get("name"),
                "lat": point["lat"],
                "lon": point["lon"],
                "h3_cell": h3.latlng_to_cell(point["lat"], point["lon"], H3_RES),
            }
        )
    df = pd.DataFrame(rows).drop_duplicates(["osm_type", "osm_id"])
    df["snapshot_date"] = date.today().isoformat()
    return df


if __name__ == "__main__":
    raw = load_pois()
    df, stats = merge_duplicates(raw)
    out = Path("data/processed/poi_snapshot.parquet")
    df.to_parquet(out, index=False)
    print(stats)
