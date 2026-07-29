class PalletConflictError(Exception):
    pass

# Helper Function
def parse_weight(weight_string):
    if not isinstance(weight_string, str):
        raise TypeError("Weight must be a string")

    try:
        if weight_string.endswith("kg"):
            return int(weight_string.replace("kg", ""))
        elif weight_string.endswith("ton"):
            return int(weight_string.replace("ton", "")) * 1000
        else:
            raise ValueError("Invalid weight format")
    except (ValueError, TypeError):
        raise
    
# Main Function
def process_shelf_assignments(request_batch, active_zones):

    
    """
    Process a batch of shelf assignment requests against a set of active warehouse zones.
 
    Returns a summary dict with:
        - successful_placements: count of fully applied requests
        - pallet_zones: {pallet_id: assigned_zone_id}
        - failed_requests: {"invalid_schema": [...], "parsing_error": [...], "pallet_conflict": [...]}
    """
    PRIORITY_ORDER = {"critical": 0, "standard": 1, "backlog": 2}
 
    # Sort: critical -> standard -> backlog. Unknown priorities sink to the end,
    # and Python's sort is stable so original relative order is preserved within a group.
    sorted_batch = sorted(
        request_batch,
        key=lambda r: PRIORITY_ORDER.get(r.get("priority"), len(PRIORITY_ORDER))
    )
 
    pallet_zones = {}
    failed_requests = {
        "invalid_schema": [],
        "parsing_error": [],
        "pallet_conflict": [],
    }
    successful_placements = 0
 
    for request in sorted_batch:
        request_id = request.get("request_id", "UNKNOWN")
        zone_id = request.get("zone_id")
 
        # Skip requests targeting zones that aren't currently active
        if zone_id not in active_zones:
            continue
 
        # --- Schema validation ---
        try:
            pallet_id = request["pallet_id"]
            weight_raw = request["max_weight"]
        except KeyError:
            failed_requests["invalid_schema"].append(request_id)
            continue
 
        # --- Weight parsing ---
        try:
            weight_kg = parse_weight(weight_raw)
        except (ValueError, TypeError):
            failed_requests["parsing_error"].append(request_id)
            continue
 
        # --- Pallet conflict check & assignment ---
        try:
            existing_zone = pallet_zones.get(pallet_id)
            if existing_zone is not None and existing_zone != zone_id:
                raise PalletConflictError(
                    f"Pallet {pallet_id} already assigned to zone {existing_zone}, "
                    f"cannot reassign to zone {zone_id} in the same batch"
                )
            pallet_zones[pallet_id] = zone_id
            successful_placements += 1
        except PalletConflictError:
            failed_requests["pallet_conflict"].append(request_id)
            continue
 
    return {
        "successful_placements": successful_placements,
        "pallet_zones": pallet_zones,
        "failed_requests": failed_requests,
    }
 
 
if __name__ == "__main__":
    import json
 
    active_zones = {"Z12", "Z13", "Z14", "Z15", "Z20"}
    request_batch = [
        {"request_id": "R01", "pallet_id": "P-2201", "zone_id": "Z12", "max_weight": "500kg", "priority": "standard"},
        {"request_id": "R02", "pallet_id": "P-9999", "zone_id": "Z99", "max_weight": "100kg", "priority": "critical"},
        {"request_id": "R03", "pallet_id": "P-2202", "zone_id": "Z13", "max_weight": "1ton", "priority": "critical"},
        {"request_id": "R04", "pallet_id": "P-2203", "zone_id": "Z14", "priority": "backlog"},
        {"request_id": "R05", "pallet_id": "P-2204", "zone_id": "Z15", "max_weight": "Full", "priority": "standard"},
        {"request_id": "R06", "pallet_id": "P-2202", "zone_id": "Z20", "max_weight": "200kg", "priority": "critical"},
    ]
 
    result = process_shelf_assignments(request_batch, active_zones)
    print(json.dumps(result, indent=2))