import re


class RoomConflictError(Exception):
    """Raised when an employee is scheduled for two different rooms within the same batch."""
    pass


def parse_duration(duration_string):
    """
    Convert a duration string like '60min' or '2hr' into an integer
    representing minutes. Assumes 1 hr = 60min.

    Raises:
        TypeError: if duration_string is not a string (e.g. None).
        ValueError: if duration_string doesn't match the expected pattern (e.g. 'TBD').
    """
    if not isinstance(duration_string, str):
        raise TypeError(f"Duration must be a string, got {type(duration_string).__name__}")

    cleaned = duration_string.strip()
    match = re.match(r'^(\d+(?:\.\d+)?)\s*(min|hr)$', cleaned, re.IGNORECASE)
    if not match:
        raise ValueError(f"Cannot parse duration string: {duration_string!r}")

    value_str, unit = match.groups()
    value = float(value_str)
    if unit.lower() == 'hr':
        value *= 60

    return int(value)


def process_room_bookings(booking_batch, active_rooms):
    """
    Process a batch of room booking requests against a set of active conference rooms.

    Returns a summary dict with:
        - successful_bookings: count of fully applied bookings
        - employee_rooms: {employee_id: assigned_room_id}
        - failed_bookings: {"invalid_schema": [...], "parsing_error": [...], "room_conflict": [...]}
    """
    TIER_ORDER = {"executive": 0, "team": 1, "personal": 2}

    # Sort: executive -> team -> personal. Unknown tiers sink to the end,
    # and Python's sort is stable so original relative order is preserved within a group.
    sorted_batch = sorted(
        booking_batch,
        key=lambda b: TIER_ORDER.get(b.get("tier"), len(TIER_ORDER))
    )

    employee_rooms = {}
    failed_bookings = {
        "invalid_schema": [],
        "parsing_error": [],
        "room_conflict": [],
    }
    successful_bookings = 0

    for booking in sorted_batch:
        booking_id = booking.get("booking_id", "UNKNOWN")
        room_id = booking.get("room_id")

        # Skip bookings targeting rooms that aren't currently active
        if room_id not in active_rooms:
            continue

        # --- Schema validation ---
        try:
            employee_id = booking["employee_id"]
            duration_raw = booking["duration"]
        except KeyError:
            failed_bookings["invalid_schema"].append(booking_id)
            continue

        # --- Duration parsing ---
        try:
            duration_min = parse_duration(duration_raw)
        except (ValueError, TypeError):
            failed_bookings["parsing_error"].append(booking_id)
            continue

        # --- Room conflict check & assignment ---
        try:
            existing_room = employee_rooms.get(employee_id)
            if existing_room is not None and existing_room != room_id:
                raise RoomConflictError(
                    f"Employee {employee_id} already assigned to room {existing_room}, "
                    f"cannot reassign to room {room_id} in the same batch"
                )
            employee_rooms[employee_id] = room_id
            successful_bookings += 1
        except RoomConflictError:
            failed_bookings["room_conflict"].append(booking_id)
            continue

    return {
        "successful_bookings": successful_bookings,
        "employee_rooms": employee_rooms,
        "failed_bookings": failed_bookings,
    }


if __name__ == "__main__":
    import json

    active_rooms = {"R01", "R02", "R03", "R05", "R08"}
    booking_batch = [
        {"booking_id": "B01", "employee_id": "E-101", "room_id": "R05", "duration": "60min", "tier": "team"},
        {"booking_id": "B02", "employee_id": "E-909", "room_id": "R99", "duration": "30min", "tier": "executive"},
        {"booking_id": "B03", "employee_id": "E-102", "room_id": "R01", "duration": "2hr", "tier": "executive"},
        {"booking_id": "B04", "employee_id": "E-103", "room_id": "R02", "tier": "personal"},
        {"booking_id": "B05", "employee_id": "E-104", "room_id": "R08", "duration": "TBD", "tier": "team"},
        {"booking_id": "B06", "employee_id": "E-102", "room_id": "R03", "duration": "45min", "tier": "executive"},
    ]

    result = process_room_bookings(booking_batch, active_rooms)
    print(json.dumps(result, indent=2))