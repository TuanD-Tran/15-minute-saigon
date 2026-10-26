from saigon15.dedup import merge_duplicates
from saigon15.pois import load_pois

raw = load_pois()
for threshold in (30, 50, 100):
    _, stats = merge_duplicates(raw, threshold)
    print(threshold, "m:", stats["before"], "->", stats["after"], stats["merged"])
