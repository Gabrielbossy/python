class CourierConflictError(Exception):
    """Raised when a courier is assigned to a second, different order in the same batch."""
    pass


def parse_distance(distance_string):
    """
    Validate and coerce a distance string like "2.3km" or "850m" into a
    standardized float in kilometers (km).
    Raises ValueError/TypeError on bad input, which the caller must handle.
    """
    if distance_string is None:
        raise TypeError("Distance string cannot be None")

    if not isinstance(distance_string, str):
        raise TypeError("Distance string must be a string")

    distance_string = distance_string.strip()

    if distance_string.endswith("km"):
        numeric_part = distance_string[:-2]
        multiplier = 1.0
    elif distance_string.endswith("m"):
        numeric_part = distance_string[:-1]
        multiplier = 0.001
    else:
        raise ValueError(f"Malformed distance string: {distance_string!r}")

    # Raises ValueError for non-numeric strings like "nearby"
    value = float(numeric_part)

    if value < 0:
        raise ValueError(f"Distance cannot be negative: {value}")

    km = value * multiplier

    if km > 15:
        raise ValueError(f"Distance {km}km exceeds max dispatch range of 15km")

    return km


def process_courier_dispatch(request_batch, available_couriers):
    TIER_ORDER = {"premium": 0, "standard": 1, "economy": 2}

    # Sort by tier priority; unknown tiers sink to the end
    sorted_batch = sorted(
        request_batch,
        key=lambda r: TIER_ORDER.get(r.get("tier"), len(TIER_ORDER))
    )

    dispatched_orders = 0
    courier_orders = {}  # courier_id -> assigned order_id
    failed_requests = {
        "invalid_schema": [],
        "parsing_error": [],
        "courier_conflict": []
    }

    for request in sorted_batch:
        req_id = request.get("req_id", "UNKNOWN")

        # Skip requests targeting couriers that aren't available — silently ignored
        courier_id = request.get("courier_id")
        if courier_id not in available_couriers:
            continue

        try:
            # Direct indexing (not .get()) so missing keys raise KeyError
            order_id = request["order_id"]
            raw_distance = request["distance"]

            # Delegate parsing/validation to the helper
            parse_distance(raw_distance)  # validated but not needed further here

            # Conflict check: same courier, different order
            if courier_id in courier_orders:
                if courier_orders[courier_id] != order_id:
                    raise CourierConflictError(
                        f"Courier {courier_id} already assigned to "
                        f"{courier_orders[courier_id]}, cannot reassign to {order_id}"
                    )
                # Same order again — harmless repeat, still counts as dispatched
            else:
                courier_orders[courier_id] = order_id

            dispatched_orders += 1

        except KeyError:
            failed_requests["invalid_schema"].append(req_id)

        except (ValueError, TypeError):
            failed_requests["parsing_error"].append(req_id)

        except CourierConflictError:
            failed_requests["courier_conflict"].append(req_id)

    return {
        "dispatched_orders": dispatched_orders,
        "courier_orders": courier_orders,
        "failed_requests": failed_requests,
    }


# --- Sample run ---
if __name__ == "__main__":
    available_couriers = {"CR_15", "CR_16", "CR_17", "CR_18", "CR_20"}

    request_batch = [
        {"req_id": "D01", "order_id": "ORD_7001", "courier_id": "CR_15", "distance": "2.3km", "tier": "standard"},
        {"req_id": "D02", "order_id": "ORD_7002", "courier_id": "CR_99", "distance": "1.1km", "tier": "premium"},
        {"req_id": "D03", "order_id": "ORD_7003", "courier_id": "CR_16", "distance": "850m", "tier": "premium"},
        {"req_id": "D04", "order_id": "ORD_7004", "courier_id": "CR_17", "tier": "economy"},
        {"req_id": "D05", "order_id": "ORD_7005", "courier_id": "CR_18", "distance": "nearby", "tier": "standard"},
        {"req_id": "D06", "order_id": "ORD_7006", "courier_id": "CR_16", "distance": "4km", "tier": "premium"},
    ]

    result = process_courier_dispatch(request_batch, available_couriers)
    import json
    print(json.dumps(result, indent=2))