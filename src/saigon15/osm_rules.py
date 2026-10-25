def classify(tags: dict) -> str | None:
    if tags.get("highway") == "bus_stop":
        return "bus_stop"
    if tags.get("public_transport") == "platform" and tags.get("bus") == "yes":
        return "bus_stop"

    amenity = tags.get("amenity")
    if amenity == "school":
        return "school"
    if amenity in {"hospital", "clinic", "doctors"}:
        return "health"
    if amenity == "marketplace":
        return "market"

    if tags.get("leisure") in {"park", "garden"}:
        return "park"

    return None
