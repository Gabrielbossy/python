class OutageTicketConflictError(Exception):
    """Raised when a substation is linked to a second, different outage ticket in the same batch."""
    pass


def parse_load(load_string):
    """
    Validate and coerce a load string like "450.5kW" or "1.2MW" into a
    standardized float in kilowatts (kW).
    Raises ValueError/TypeError on bad input, which the caller must handle.
    """
    if load_string is None:
        raise TypeError("Load string cannot be None")

    if not isinstance(load_string, str):
        raise TypeError("Load string must be a string")

    load_string = load_string.strip()

    if load_string.endswith("MW"):
        numeric_part = load_string[:-2]
        multiplier = 1000.0
    elif load_string.endswith("kW"):
        numeric_part = load_string[:-2]
        multiplier = 1.0
    else:
        raise ValueError(f"Malformed load string: {load_string!r}")

    # Raises ValueError for non-numeric strings like "TBD"
    value = float(numeric_part)

    if value < 0:
        raise ValueError(f"Load cannot be negative: {value}")

    return value * multiplier


def process_load_shedding(request_batch, online_substations):
    TIER_ORDER = {"emergency": 0, "scheduled": 1, "voluntary": 2}

    # Sort by tier priority; unknown tiers sink to the end
    sorted_batch = sorted(
        request_batch,
        key=lambda r: TIER_ORDER.get(r.get("tier"), len(TIER_ORDER))
    )

    shed_substations = 0
    substation_tickets = {}  # substation_id -> assigned outage_ticket
    failed_requests = {
        "invalid_schema": [],
        "parsing_error": [],
        "ticket_conflict": []
    }

    for request in sorted_batch:
        req_id = request.get("req_id", "UNKNOWN")

        # Skip requests targeting substations that aren't online — silently ignored
        substation_id = request.get("substation_id")
        if substation_id not in online_substations:
            continue

        try:
            # Direct indexing (not .get()) so missing keys raise KeyError
            outage_ticket = request["outage_ticket"]
            raw_load = request["load_kw"]

            # Delegate parsing/validation to the helper
            parse_load(raw_load)  # validated but not needed further here

            # Conflict check: same substation, different ticket
            if substation_id in substation_tickets:
                if substation_tickets[substation_id] != outage_ticket:
                    raise OutageTicketConflictError(
                        f"Substation {substation_id} already linked to "
                        f"{substation_tickets[substation_id]}, cannot reassign to {outage_ticket}"
                    )
                # Same ticket again — harmless repeat, still counts as shed
            else:
                substation_tickets[substation_id] = outage_ticket

            shed_substations += 1

        except KeyError:
            failed_requests["invalid_schema"].append(req_id)

        except (ValueError, TypeError):
            failed_requests["parsing_error"].append(req_id)

        except OutageTicketConflictError:
            failed_requests["ticket_conflict"].append(req_id)

    return {
        "shed_substations": shed_substations,
        "substation_tickets": substation_tickets,
        "failed_requests": failed_requests,
    }


# --- Sample run ---
if __name__ == "__main__":
    online_substations = {"SUB_204", "SUB_205", "SUB_206", "SUB_207", "SUB_300"}

    request_batch = [
        {"req_id": "G01", "substation_id": "SUB_204", "outage_ticket": "OUT-8001", "load_kw": "450.5kW", "tier": "scheduled"},
        {"req_id": "G02", "substation_id": "SUB_999", "outage_ticket": "OUT-8002", "load_kw": "300kW", "tier": "emergency"},
        {"req_id": "G03", "substation_id": "SUB_205", "outage_ticket": "OUT-8003", "load_kw": "1.2MW", "tier": "emergency"},
        {"req_id": "G04", "substation_id": "SUB_206", "load_kw": "200kW", "tier": "voluntary"},
        {"req_id": "G05", "substation_id": "SUB_207", "outage_ticket": "OUT-8004", "load_kw": "TBD", "tier": "scheduled"},
        {"req_id": "G06", "substation_id": "SUB_205", "outage_ticket": "OUT-8005", "load_kw": "800kW", "tier": "emergency"},
    ]

    result = process_load_shedding(request_batch, online_substations)
    import json
    print(json.dumps(result, indent=2))