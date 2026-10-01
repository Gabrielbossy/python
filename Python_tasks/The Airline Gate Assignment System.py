class GateConflictError(Exception):
    """Raised when a flight is assigned to a second, different gate in the same batch."""
    pass


def parse_turnaround(turnaround_string):
    """
    Validate and coerce a turnaround string like "45min" or "1hr" into
    a standardized integer number of minutes.
    Raises ValueError/TypeError on bad input, which the caller must handle.
    """
    if turnaround_string is None:
        raise TypeError("Turnaround string cannot be None")

    if not isinstance(turnaround_string, str):
        raise TypeError("Turnaround string must be a string")

    turnaround_string = turnaround_string.strip()

    if turnaround_string.endswith("hr"):
        numeric_part = turnaround_string[:-2]
        multiplier = 60
    elif turnaround_string.endswith("min"):
        numeric_part = turnaround_string[:-3]
        multiplier = 1
    else:
        raise ValueError(f"Malformed turnaround string: {turnaround_string!r}")

    # Raises ValueError for non-numeric strings like "soon"
    value = int(numeric_part)

    minutes = value * multiplier

    if not (0 < minutes <= 180):
        raise ValueError(f"Turnaround {minutes} out of valid range (1-180 minutes)")

    return minutes


def process_gate_assignments(request_batch, free_gates):
    CLASS_ORDER = {"international": 0, "domestic": 1, "cargo": 2}

    # Sort by class priority; unknown classes sink to the end
    sorted_batch = sorted(
        request_batch,
        key=lambda r: CLASS_ORDER.get(r.get("class"), len(CLASS_ORDER))
    )

    assigned_flights = 0
    flight_gates = {}  # flight_id -> assigned gate
    failed_requests = {
        "invalid_schema": [],
        "parsing_error": [],
        "gate_conflict": []
    }

    for request in sorted_batch:
        req_id = request.get("req_id", "UNKNOWN")

        # Skip requests targeting gates that aren't free — silently ignored
        gate = request.get("gate")
        if gate not in free_gates:
            continue

        try:
            # Direct indexing (not .get()) so missing keys raise KeyError
            flight_id = request["flight_id"]
            raw_turnaround = request["turnaround"]

            # Delegate parsing/validation to the helper
            parse_turnaround(raw_turnaround)  # validated but not needed further here

            # Conflict check: same flight, different gate
            if flight_id in flight_gates:
                if flight_gates[flight_id] != gate:
                    raise GateConflictError(
                        f"Flight {flight_id} already assigned to "
                        f"{flight_gates[flight_id]}, cannot reassign to {gate}"
                    )
                # Same gate again — harmless repeat, still counts as assigned
            else:
                flight_gates[flight_id] = gate

            assigned_flights += 1

        except KeyError:
            failed_requests["invalid_schema"].append(req_id)

        except (ValueError, TypeError):
            failed_requests["parsing_error"].append(req_id)

        except GateConflictError:
            failed_requests["gate_conflict"].append(req_id)

    return {
        "assigned_flights": assigned_flights,
        "flight_gates": flight_gates,
        "failed_requests": failed_requests,
    }


# --- Sample run ---
if __name__ == "__main__":
    free_gates = {"B12", "B13", "C04", "C05", "A01"}

    request_batch = [
        {"req_id": "GA01", "flight_id": "FL_2201", "gate": "B12", "turnaround": "45min", "class": "domestic"},
        {"req_id": "GA02", "flight_id": "FL_2202", "gate": "D99", "turnaround": "30min", "class": "international"},
        {"req_id": "GA03", "flight_id": "FL_2203", "gate": "C04", "turnaround": "1hr", "class": "international"},
        {"req_id": "GA04", "flight_id": "FL_2204", "gate": "A01", "class": "cargo"},
        {"req_id": "GA05", "flight_id": "FL_2205", "gate": "B13", "turnaround": "soon", "class": "domestic"},
        {"req_id": "GA06", "flight_id": "FL_2203", "gate": "B12", "turnaround": "50min", "class": "international"},
    ]

    result = process_gate_assignments(request_batch, free_gates)
    import json
    print(json.dumps(result, indent=2))