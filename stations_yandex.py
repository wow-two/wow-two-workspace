

def merge_metro() -> None:
    """OSM metro as the base, the official file only where it adds a station.

    OSM carries 49 stations against the official file's 36. The 14 it holds alone
    are the Ring line, which the 2025-09-30 Yandex snapshot either predates or
    classes as surface rail — dropping to 36 would delete a whole line from the
    network. The official file adds exactly one station OSM lacks, `Sergeli`.

    Positions are taken from OSM even where both agree, because the 35 shared
    names sit a median 12 m apart. Inside a 1 km catchment that is noise, and the
    OSM points are already the ones the walk graph was snapped against.
    """
    import re
    import unicodedata

    def key(name: str | None) -> str:
        if not name:
            return ""
        text = unicodedata.normalize("NFKD", name).lower()
        for ch in "ʻʼ‘’":
            text = text.replace(ch, "'")
        return re.sub(r"[^a-z0-9]", "", text)

    points = os.path.join(
        ROOT, "..", "engineering", "codebase", "nth26.frontend-services",
        "apps", "studio", "public", "data",
    )
    with open(os.path.join(points, "metro-stations.geojson"), encoding="utf-8") as handle:
        osm = json.load(handle)["features"]
    with open(os.path.join(BUILD, "metro-stations-official.geojson"), encoding="utf-8") as handle:
        official = json.load(handle)["features"]

    seen = {key(f["properties"].get("name")) for f in osm}
    added = [f for f in official if key(f["properties"].get("name")) not in seen]
    merged = osm + added

    write(os.path.join(BUILD, "metro-stations-merged.geojson"), merged)
    print(f"\nmetro merge: {len(osm)} OSM + {len(added)} official-only = {len(merged)}")
    for f in added:
        print(f"  added {f['properties']['name']}")


if __name__ == "__main__":
    merge_metro()
