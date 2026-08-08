import re


class WardConflictError(Exception):
    """Raised when a patient is scheduled for two different wards within the same batch."""
    pass


def parse_stay_duration(duration_string):
    """
    Convert a stay duration string like '3days' or '12hrs' into an integer
    representing hours. Assumes 1 day = 24hrs.

    Raises:
        TypeError: if duration_string is not a string (e.g. None).
        ValueError: if duration_string doesn't match the expected pattern (e.g. 'Unknown').
    """
    if not isinstance(duration_string, str):
        raise TypeError(f"Stay duration must be a string, got {type(duration_string).__name__}")

    cleaned = duration_string.strip()
    match = re.match(r'^(\d+(?:\.\d+)?)\s*(days|hrs)$', cleaned, re.IGNORECASE)
    if not match:
        raise ValueError(f"Cannot parse stay duration string: {duration_string!r}")

    value_str, unit = match.groups()
    value = float(value_str)
    if unit.lower() == 'days':
        value *= 24

    return int(value)


def process_bed_assignments(admission_batch, active_wards):
    """
    Process a batch of patient admission requests against a set of active hospital wards.

    Returns a summary dict with:
        - successful_admissions: count of fully applied admissions
        - patient_wards: {patient_id: assigned_ward_id}
        - failed_admissions: {"invalid_schema": [...], "parsing_error": [...], "ward_conflict": [...]}
    """
    SEVERITY_ORDER = {"emergency": 0, "urgent": 1, "routine": 2}

    # Sort: emergency -> urgent -> routine. Unknown severities sink to the end,
    # and Python's sort is stable so original relative order is preserved within a group.
    sorted_batch = sorted(
        admission_batch,
        key=lambda a: SEVERITY_ORDER.get(a.get("severity"), len(SEVERITY_ORDER))
    )

    patient_wards = {}
    failed_admissions = {
        "invalid_schema": [],
        "parsing_error": [],
        "ward_conflict": [],
    }
    successful_admissions = 0

    for admission in sorted_batch:
        request_id = admission.get("request_id", "UNKNOWN")
        ward_id = admission.get("ward_id")

        # Skip admissions targeting wards that aren't currently active
        if ward_id not in active_wards:
            continue

        # --- Schema validation ---
        try:
            patient_id = admission["patient_id"]
            duration_raw = admission["stay_duration"]
        except KeyError:
            failed_admissions["invalid_schema"].append(request_id)
            continue

        # --- Duration parsing ---
        try:
            duration_hrs = parse_stay_duration(duration_raw)
        except (ValueError, TypeError):
            failed_admissions["parsing_error"].append(request_id)
            continue

        # --- Ward conflict check & assignment ---
        try:
            existing_ward = patient_wards.get(patient_id)
            if existing_ward is not None and existing_ward != ward_id:
                raise WardConflictError(
                    f"Patient {patient_id} already assigned to ward {existing_ward}, "
                    f"cannot reassign to ward {ward_id} in the same batch"
                )
            patient_wards[patient_id] = ward_id
            successful_admissions += 1
        except WardConflictError:
            failed_admissions["ward_conflict"].append(request_id)
            continue

    return {
        "successful_admissions": successful_admissions,
        "patient_wards": patient_wards,
        "failed_admissions": failed_admissions,
    }


if __name__ == "__main__":
    import json

    active_wards = {"W01", "W02", "W03", "W04", "W07"}
    admission_batch = [
        {"request_id": "H01", "patient_id": "P-3001", "ward_id": "W04", "stay_duration": "3days", "severity": "urgent"},
        {"request_id": "H02", "patient_id": "P-3009", "ward_id": "W99", "stay_duration": "12hrs", "severity": "emergency"},
        {"request_id": "H03", "patient_id": "P-3002", "ward_id": "W01", "stay_duration": "48hrs", "severity": "emergency"},
        {"request_id": "H04", "patient_id": "P-3003", "ward_id": "W02", "severity": "routine"},
        {"request_id": "H05", "patient_id": "P-3004", "ward_id": "W07", "stay_duration": "Unknown", "severity": "urgent"},
        {"request_id": "H06", "patient_id": "P-3002", "ward_id": "W03", "stay_duration": "6hrs", "severity": "emergency"},
    ]

    result = process_bed_assignments(admission_batch, active_wards)
    print(json.dumps(result, indent=2))