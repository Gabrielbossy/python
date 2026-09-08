class DuplicateShipmentError(Exception):
    """Raised when an order attempts a second dispatch in the same batch."""
    pass


def parse_weight(weight_value):
    """
    Validate and coerce a shipment weight.
    Raises ValueError/TypeError on bad input, which the caller must handle.
    """
    if weight_value is None:
        raise TypeError("Weight cannot be None")

    # Raises ValueError for strings like "heavy",
    # TypeError for unsupported types (e.g. list, dict)
    weight = float(weight_value)

    if weight <= 0:
        raise ValueError("Weight must be greater than zero")

    return weight


def process_shipment_queue(shipment_batch, dock_capacities):
    URGENCY_ORDER = {"express": 0, "standard": 1, "deferred": 2}

    # Sort by urgency priority; unknown urgencies sink to the end
    sorted_batch = sorted(
        shipment_batch,
        key=lambda r: URGENCY_ORDER.get(r.get("urgency"), len(URGENCY_ORDER))
    )

    dispatched_shipments = []
    denied_capacity = []
    failed_requests = {"data_error": [], "policy_violation": []}
    shipped_orders = set()  # Set of order_ids already dispatched this batch

    for request in sorted_batch:
        req_id = request.get("req_id", "UNKNOWN")

        try:
            # Direct indexing (not .get()) so missing keys raise KeyError
            dock = request["dock"]
            raw_weight = request["weight"]
            order_id = request["order_id"]

            # Delegate type/value validation to the helper
            weight = parse_weight(raw_weight)

            # Duplicate-shipment check
            if order_id in shipped_orders:
                raise DuplicateShipmentError(
                    f"Order {order_id} already dispatched this batch"
                )

            # Capacity check
            if dock not in dock_capacities or weight > dock_capacities[dock]:
                denied_capacity.append(req_id)
                continue

            # Approve
            dock_capacities[dock] -= weight
            shipped_orders.add(order_id)
            dispatched_shipments.append(req_id)

        except KeyError:
            failed_requests["data_error"].append(req_id)

        except (ValueError, TypeError):
            failed_requests["data_error"].append(req_id)

        except DuplicateShipmentError:
            failed_requests["policy_violation"].append(req_id)

    return {
        "dispatched_shipments": dispatched_shipments,
        "denied_capacity": denied_capacity,
        "failed_requests": failed_requests,
        "remaining_capacities": dock_capacities,
    }


# --- Sample run ---
if __name__ == "__main__":
    dock_capacities = {
        "Dock_A": 200,
        "Dock_B": 150
    }

    shipment_batch = [
        {"req_id": "S01", "order_id": "ORD_01", "dock": "Dock_A", "weight": 80, "urgency": "standard"},
        {"req_id": "S02", "order_id": "ORD_02", "dock": "Dock_B", "weight": "heavy", "urgency": "express"},
        {"req_id": "S03", "order_id": "ORD_03", "weight": 40, "urgency": "standard"},
        {"req_id": "S04", "order_id": "ORD_01", "dock": "Dock_B", "weight": 60, "urgency": "deferred"},
        {"req_id": "S05", "order_id": "ORD_05", "dock": "Dock_A", "weight": 150, "urgency": "express"},
        {"req_id": "S06", "order_id": "ORD_06", "dock": "Dock_B", "weight": 0, "urgency": "standard"},
    ]

    result = process_shipment_queue(shipment_batch, dock_capacities)
    import json
    print(json.dumps(result, indent=2))