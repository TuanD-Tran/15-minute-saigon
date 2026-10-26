from saigon15.dedup import merge_duplicates, normalize_name
from saigon15.pois import load_pois

raw = load_pois()
merged, stats = merge_duplicates(raw, 50)

before = raw.groupby("category").size()
after = merged.groupby("category").size()
unnamed = raw[raw["name"].map(normalize_name).isna()].groupby("category").size()

print("| Loại | Số điểm thô | Sau khi gộp | Bị gộp | Tỷ lệ gộp | Không có tên |")
print("| --- | --- | --- | --- | --- | --- |")
for cat in before.index:
    b, a = int(before[cat]), int(after[cat])
    n_unnamed = int(unnamed.get(cat, 0))
    print(f"| {cat} | {b} | {a} | {b - a} | {100 * (b - a) / b:.1f}% | {n_unnamed} |")
