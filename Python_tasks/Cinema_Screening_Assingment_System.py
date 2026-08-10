import re


class ScreenConflictError(Exception):
    """Raised when a movie is scheduled for two different screens within the same batch."""
    pass


def parse_runtime(runtime_string):
    """
    Convert a runtime string like '120min' or '2hr' into an integer
    representing minutes. Assumes 1 hr = 60min.

    Raises:
        TypeError: if runtime_string is not a string (e.g. None).
        ValueError: if runtime_string doesn't match the expected pattern (e.g. 'N/A').
    """
    if not isinstance(runtime_string, str):
        raise TypeError(f"Runtime must be a string, got {type(runtime_string).__name__}")

    cleaned = runtime_string.strip()
    match = re.match(r'^(\d+(?:\.\d+)?)\s*(min|hr)$', cleaned, re.IGNORECASE)
    if not match:
        raise ValueError(f"Cannot parse runtime string: {runtime_string!r}")

    value_str, unit = match.groups()
    value = float(value_str)
    if unit.lower() == 'hr':
        value *= 60

    return int(value)


def process_screenings(screening_batch, active_screens):
    """
    Process a batch of screening requests against a set of active theater screens.

    Returns a summary dict with:
        - successful_screenings: count of fully applied screenings
        - movie_screens: {movie_id: assigned_screen_id}
        - failed_screenings: {"invalid_schema": [...], "parsing_error": [...], "screen_conflict": [...]}
    """
    TIER_ORDER = {"premiere": 0, "standard": 1, "matinee": 2}

    # Sort: premiere -> standard -> matinee. Unknown tiers sink to the end,
    # and Python's sort is stable so original relative order is preserved within a group.
    sorted_batch = sorted(
        screening_batch,
        key=lambda s: TIER_ORDER.get(s.get("release_tier"), len(TIER_ORDER))
    )

    movie_screens = {}
    failed_screenings = {
        "invalid_schema": [],
        "parsing_error": [],
        "screen_conflict": [],
    }
    successful_screenings = 0

    for screening in sorted_batch:
        screening_id = screening.get("screening_id", "UNKNOWN")
        screen_id = screening.get("screen_id")

        # Skip screenings targeting screens that aren't currently active
        if screen_id not in active_screens:
            continue

        # --- Schema validation ---
        try:
            movie_id = screening["movie_id"]
            runtime_raw = screening["runtime"]
        except KeyError:
            failed_screenings["invalid_schema"].append(screening_id)
            continue

        # --- Runtime parsing ---
        try:
            runtime_min = parse_runtime(runtime_raw)
        except (ValueError, TypeError):
            failed_screenings["parsing_error"].append(screening_id)
            continue

        # --- Screen conflict check & assignment ---
        try:
            existing_screen = movie_screens.get(movie_id)
            if existing_screen is not None and existing_screen != screen_id:
                raise ScreenConflictError(
                    f"Movie {movie_id} already assigned to screen {existing_screen}, "
                    f"cannot reassign to screen {screen_id} in the same batch"
                )
            movie_screens[movie_id] = screen_id
            successful_screenings += 1
        except ScreenConflictError:
            failed_screenings["screen_conflict"].append(screening_id)
            continue

    return {
        "successful_screenings": successful_screenings,
        "movie_screens": movie_screens,
        "failed_screenings": failed_screenings,
    }


if __name__ == "__main__":
    import json

    active_screens = {"SC1", "SC2", "SC3", "SC4", "SC8"}
    screening_batch = [
        {"screening_id": "S01", "movie_id": "M-401", "screen_id": "SC3", "runtime": "120min", "release_tier": "standard"},
        {"screening_id": "S02", "movie_id": "M-909", "screen_id": "SC9", "runtime": "90min", "release_tier": "premiere"},
        {"screening_id": "S03", "movie_id": "M-402", "screen_id": "SC1", "runtime": "2hr", "release_tier": "premiere"},
        {"screening_id": "S04", "movie_id": "M-403", "screen_id": "SC2", "release_tier": "matinee"},
        {"screening_id": "S05", "movie_id": "M-404", "screen_id": "SC8", "runtime": "N/A", "release_tier": "standard"},
        {"screening_id": "S06", "movie_id": "M-402", "screen_id": "SC4", "runtime": "100min", "release_tier": "premiere"},
    ]

    result = process_screenings(screening_batch, active_screens)
    print(json.dumps(result, indent=2))