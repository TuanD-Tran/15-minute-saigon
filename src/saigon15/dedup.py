import unicodedata

import pandas as pd

from saigon15.config import DEDUP_THRESHOLD_M
from saigon15.geo import haversine_m


def normalize_name(name) -> str | None:
    if not isinstance(name, str) or not name.strip():
        return None
    text = name.strip().lower().replace("đ", "d")
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    return " ".join(text.split())


class UnionFind:
    def __init__(self, n: int) -> None:
        self.parent = list(range(n))

    def find(self, i: int) -> int:
        while self.parent[i] != i:
            self.parent[i] = self.parent[self.parent[i]]
            i = self.parent[i]
        return i

    def union(self, i: int, j: int) -> None:
        ri, rj = self.find(i), self.find(j)
        if ri != rj:
            self.parent[rj] = ri


def merge_duplicates(df: pd.DataFrame, threshold_m: float = DEDUP_THRESHOLD_M):
    df = df.reset_index(drop=True).copy()
    df["name_norm"] = df["name"].map(normalize_name)
    uf = UnionFind(len(df))

    named = df[df["name_norm"].notna()]
    for _, group in named.groupby(["category", "name_norm"]):
        idx = list(group.index)
        for a in range(len(idx)):
            for b in range(a + 1, len(idx)):
                i, j = idx[a], idx[b]
                dist = haversine_m(
                    df.at[i, "lat"], df.at[i, "lon"], df.at[j, "lat"], df.at[j, "lon"]
                )
                if dist < threshold_m:
                    uf.union(i, j)

    df["cluster"] = [uf.find(i) for i in range(len(df))]
    df["_not_node"] = df["osm_type"] != "node"
    kept = (
        df.sort_values(["cluster", "_not_node", "osm_id"])
        .drop_duplicates("cluster", keep="first")
        .sort_index()
    )

    merged_by_cat = (
        (df.groupby("category").size() - kept.groupby("category").size()).fillna(0).astype(int)
    )
    stats = {
        "before": len(df),
        "after": len(kept),
        "merged": merged_by_cat.to_dict(),
        "unnamed": int(df["name_norm"].isna().sum()),
    }
    return kept.drop(columns=["cluster", "_not_node"]), stats
