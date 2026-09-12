class OverlappingBookingError(Exception):
    """Raised when an employee attempts a second room booking in the same batch."""
    pass


def parse_minutes(minutes_value):
    """
    Validate and coerce a requested meeting length.
    Raises ValueError/TypeError on bad input, which the caller must handle.
    """
    if minutes_value is None:
        raise TypeError("Minutes cannot be None")

    # Raises ValueError for strings like "half an hour",
    # TypeError for unsupported types (e.g. list, dict)
    minutes = float(minutes_value)

    if minutes <= 0:
        raise ValueError("Minutes must be greater than zero")

    if minutes > 240:
        raise ValueError("Minutes exceeds max single-meeting length of 240")

    return minutes


def process_room_reservations(reservation_batch, room_availability):
    LEVEL_ORDER = {"executive": 0, "team": 1, "individual": 2}

    # Sort by level priority; unknown levels sink to the end
    sorted_batch = sorted(
        reservation_batch,
        key=lambda r: LEVEL_ORDER.get(r.get("level"), len(LEVEL_ORDER))
    )

    confirmed_reservations = []
    denied_availability = []
    failed_requests = {"data_error": [], "policy_violation": []}
    booked_employees = set()  # Set of employee_ids who already secured a room

    for request in sorted_batch:
        req_id = request.get("req_id", "UNKNOWN")

        try:
            # Direct indexing (not .get()) so missing keys raise KeyError
            room = request["room"]
            raw_minutes = request["minutes"]
            employee_id = request["employee_id"]

            # Delegate type/value validation to the helper
            minutes = parse_minutes(raw_minutes)

            # Overlap / double-booking check
            if employee_id in booked_employees:
                raise OverlappingBookingError(
                    f"Employee {employee_id} already booked a room this batch"
                )

            # Availability check
            if room not in room_availability or minutes > room_availability[room]:
                denied_availability.append(req_id)
                continue

            # Confirm
            room_availability[room] -= minutes
            booked_employees.add(employee_id)
            confirmed_reservations.append(req_id)

        except KeyError:
            failed_requests["data_error"].append(req_id)

        except (ValueError, TypeError):
            failed_requests["data_error"].append(req_id)

        except OverlappingBookingError:
            failed_requests["policy_violation"].append(req_id)

    return {
        "confirmed_reservations": confirmed_reservations,
        "denied_availability": denied_availability,
        "failed_requests": failed_requests,
        "remaining_availability": room_availability,
    }


# --- Sample run ---
if __name__ == "__main__":
    room_availability = {
        "Boardroom_1": 90,
        "Huddle_2": 120
    }

    reservation_batch = [
        {"req_id": "M01", "employee_id": "EMP_01", "room": "Boardroom_1", "minutes": 60, "level": "team"},
        {"req_id": "M02", "employee_id": "EMP_02", "room": "Huddle_2", "minutes": "half an hour", "level": "executive"},
        {"req_id": "M03", "employee_id": "EMP_03", "minutes": 45, "level": "team"},
        {"req_id": "M04", "employee_id": "EMP_01", "room": "Huddle_2", "minutes": 30, "level": "individual"},
        {"req_id": "M05", "employee_id": "EMP_05", "room": "Boardroom_1", "minutes": 45, "level": "executive"},
        {"req_id": "M06", "employee_id": "EMP_06", "room": "Huddle_2", "minutes": 300, "level": "team"},
    ]

    result = process_room_reservations(reservation_batch, room_availability)
    import json
    print(json.dumps(result, indent=2))