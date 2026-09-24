class WardConflictError(Exception):
    """Raised when a patient is assigned to a second, different ward in the same batch."""
    pass


def parse_age(age_value):
    """
    Validate and coerce a patient age value like "67" into an int
    within a realistic human range of 0-120.
    Raises ValueError/TypeError on bad input, which the caller must handle.
    """
    if age_value is None:
        raise TypeError("Age cannot be None")

    # Raises ValueError for strings like "unknown",
    # TypeError for unsupported types (e.g. list, dict)
    age = int(age_value)

    if not (0 <= age <= 120):
        raise ValueError(f"Age {age} out of realistic range (0-120)")

    return age


def process_bed_assignments(request_batch, available_wards):
    CONDITION_ORDER = {"critical": 0, "serious": 1, "stable": 2}

    # Sort by condition priority; unknown conditions sink to the end
    sorted_batch = sorted(
        request_batch,
        key=lambda r: CONDITION_ORDER.get(r.get("condition"), len(CONDITION_ORDER))
    )

    admitted_patients = 0
    patient_wards = {}  # patient_id -> assigned ward
    failed_requests = {
        "invalid_schema": [],
        "parsing_error": [],
        "ward_conflict": []
    }

    for request in sorted_batch:
        request_id = request.get("request_id", "UNKNOWN")

        # Skip requests targeting wards without open beds — silently ignored
        ward = request.get("ward")
        if ward not in available_wards:
            continue

        try:
            # Direct indexing (not .get()) so missing keys raise KeyError
            patient_id = request["patient_id"]
            raw_age = request["age"]

            # Delegate parsing/validation to the helper
            parse_age(raw_age)  # validated but not needed further here

            # Conflict check: same patient, different ward
            if patient_id in patient_wards:
                if patient_wards[patient_id] != ward:
                    raise WardConflictError(
                        f"Patient {patient_id} already assigned to "
                        f"{patient_wards[patient_id]}, cannot reassign to {ward}"
                    )
                # Same ward again — harmless repeat, still counts as admitted
            else:
                patient_wards[patient_id] = ward

            admitted_patients += 1

        except KeyError:
            failed_requests["invalid_schema"].append(request_id)

        except (ValueError, TypeError):
            failed_requests["parsing_error"].append(request_id)

        except WardConflictError:
            failed_requests["ward_conflict"].append(request_id)

    return {
        "admitted_patients": admitted_patients,
        "patient_wards": patient_wards,
        "failed_requests": failed_requests,
    }


# --- Sample run ---
if __name__ == "__main__":
    available_wards = {"ICU", "Cardiology", "General", "Pediatrics", "Maternity"}

    request_batch = [
        {"request_id": "P01", "patient_id": "PT_5001", "ward": "ICU", "age": "67", "condition": "serious"},
        {"request_id": "P02", "patient_id": "PT_5002", "ward": "Oncology", "age": "45", "condition": "critical"},
        {"request_id": "P03", "patient_id": "PT_5003", "ward": "ICU", "age": "34", "condition": "critical"},
        {"request_id": "P04", "patient_id": "PT_5004", "ward": "General", "condition": "stable"},
        {"request_id": "P05", "patient_id": "PT_5005", "ward": "Cardiology", "age": "unknown", "condition": "serious"},
        {"request_id": "P06", "patient_id": "PT_5003", "ward": "Cardiology", "age": "34", "condition": "critical"},
    ]

    result = process_bed_assignments(request_batch, available_wards)
    import json
    print(json.dumps(result, indent=2))