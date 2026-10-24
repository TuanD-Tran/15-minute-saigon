import hashlib
import json
import time
from datetime import date
from pathlib import Path

import requests

from saigon15.config import BBOX

URL = "https://overpass-api.de/api/interpreter"
RAW = Path("data/raw")
B = ",".join(str(x) for x in BBOX)

POI_QUERY = f"""[out:json][timeout:120];
(
  node["highway"="bus_stop"]({B});
  node["public_transport"="platform"]["bus"="yes"]({B});
  nwr["amenity"~"^(school|hospital|clinic|doctors|marketplace)$"]({B});
  nwr["leisure"~"^(park|garden)$"]({B});
);
out center tags;"""

ROAD_QUERY = f"""[out:json][timeout:180];
way["highway"]({B});
out geom tags;"""


def fetch(name: str, query: str, retries: int = 3) -> dict:
    RAW.mkdir(parents=True, exist_ok=True)
    headers = {"User-Agent": "saigon15-student-project/0.1"}

    for attempt in range(retries):
        resp = requests.post(URL, data={"data": query}, headers=headers, timeout=300)

        if resp.status_code == 200:
            break
        time.sleep(10 * (attempt + 1))
    else:
        resp.raise_for_status()
    path = RAW / f"{name}.json"
    path.write_bytes(resp.content)
    payload = resp.json()
    return {
        "file": str(path),
        "sha256": hashlib.sha256(resp.content).hexdigest(),
        "osm_base_timestamp": payload.get("osm3s", {}).get("timestamp_osm_base"),
        "n_elements": len(payload["elements"]),
    }


def main() -> None:
    log = {
        "downloaded_on": date.today().isoformat(),
        "bbox": BBOX,
        "source": URL,
        "files": [fetch("pois", POI_QUERY), fetch("roads", ROAD_QUERY)],
    }
    Path("data/source_log.json").write_text(json.dumps(log, indent=2), encoding="utf-8")
    print(json.dumps(log, indent=2))


if __name__ == "__main__":
    main()
