import re


class GateConflictError(Exception):
    """Raised when a flight is scheduled for two different gates within the same batch."""
    pass


def parse_fuel_load(fuel_string):
    """
    Convert a fuel load string like '5000L' or '5kL' into an integer
    representing liters (L). Assumes 1 kL = 1000L.

    Raises:
        TypeError: if fuel_string is not a string (e.g. None).
        ValueError: if fuel_string doesn't match the expected pattern (e.g. 'Full').
    """
    if not isinstance(fuel_string, str):
        raise TypeError(f"Fuel load must be a string, got {type(fuel_string).__name__}")

    cleaned = fuel_string.strip()
    match = re.match(r'^(\d+(?:\.\d+)?)\s*(kL|L)$', cleaned, re.IGNORECASE)
    if not match:
        raise ValueError(f"Cannot parse fuel load string: {fuel_string!r}")

    value_str, unit = match.groups()
    value = float(value_str)
    if unit.lower() == 'kl':
        value *= 1000

    return int(value)


def process_gate_assignments(assignment_batch, active_gates):
    """
    Process a batch of gate assignment requests against a set of active airport gates.

    Returns a summary dict with:
        - successful_assignments: count of fully applied assignments
        - flight_gates: {flight_id: assigned_gate_id}
        - failed_assignments: {"invalid_schema": [...], "parsing_error": [...], "gate_conflict": [...]}
    """
    FLIGHT_TYPE_ORDER = {"international": 0, "domestic": 1, "regional": 2}

    # Sort: international -> domestic -> regional. Unknown types sink to the end,
    # and Python's sort is stable so original relative order is preserved within a group.
    sorted_batch = sorted(
        assignment_batch,
        key=lambda a: FLIGHT_TYPE_ORDER.get(a.get("flight_type"), len(FLIGHT_TYPE_ORDER))
    )

    flight_gates = {}
    failed_assignments = {
        "invalid_schema": [],
        "parsing_error": [],
        "gate_conflict": [],
    }
    successful_assignments = 0

    for assignment in sorted_batch:
        assignment_id = assignment.get("assignment_id", "UNKNOWN")
        gate_id = assignment.get("gate_id")

        # Skip assignments targeting gates that aren't currently active
        if gate_id not in active_gates:
            continue

        # --- Schema validation ---
        try:
            flight_id = assignment["flight_id"]
            fuel_raw = assignment["fuel_load"]
        except KeyError:
            failed_assignments["invalid_schema"].append(assignment_id)
            continue

        # --- Fuel load parsing ---
        try:
            fuel_liters = parse_fuel_load(fuel_raw)
        except (ValueError, TypeError):
            failed_assignments["parsing_error"].append(assignment_id)
            continue

        # --- Gate conflict check & assignment ---
        try:
            existing_gate = flight_gates.get(flight_id)
            if existing_gate is not None and existing_gate != gate_id:
                raise GateConflictError(
                    f"Flight {flight_id} already assigned to gate {existing_gate}, "
                    f"cannot reassign to gate {gate_id} in the same batch"
                )
            flight_gates[flight_id] = gate_id
            successful_assignments += 1
        except GateConflictError:
            failed_assignments["gate_conflict"].append(assignment_id)
            continue

    return {
        "successful_assignments": successful_assignments,
        "flight_gates": flight_gates,
        "failed_assignments": failed_assignments,
    }


if __name__ == "__main__":
    import json

    active_gates = {"A1", "A2", "A5", "B3", "B7"}
    assignment_batch = [
        {"assignment_id": "G01", "flight_id": "FL-220", "gate_id": "A5", "fuel_load": "5000L", "flight_type": "domestic"},
        {"assignment_id": "G02", "flight_id": "FL-909", "gate_id": "C1", "fuel_load": "3000L", "flight_type": "international"},
        {"assignment_id": "G03", "flight_id": "FL-221", "gate_id": "A1", "fuel_load": "6kL", "flight_type": "international"},
        {"assignment_id": "G04", "flight_id": "FL-222", "gate_id": "A2", "flight_type": "regional"},
        {"assignment_id": "G05", "flight_id": "FL-223", "gate_id": "B7", "fuel_load": "Full", "flight_type": "domestic"},
        {"assignment_id": "G06", "flight_id": "FL-221", "gate_id": "B3", "fuel_load": "4500L", "flight_type": "international"},
    ]

    result = process_gate_assignments(assignment_batch, active_gates)
    print(json.dumps(result, indent=2))