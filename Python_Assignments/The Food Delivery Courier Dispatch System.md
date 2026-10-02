The Problem: The Food Delivery Courier Dispatch System

Background:
You are building an automated pipeline for a food delivery platform that assigns incoming orders to available couriers in a city zone. Different restaurant partners submit dispatch requests asynchronously throughout the lunch rush. Your script must process these requests, parse the string-based delivery distance into usable floats, and prevent a courier from being double-booked on two conflicting orders at once.

The Input:
You receive a list of request dictionaries and a Set of courier IDs currently available for dispatch. A valid request looks like this:

python
{"req_id": "D01", "order_id": "ORD_7001", "courier_id": "CR_15", "distance": "2.3km", "tier": "premium"}

The Requirements:

1. Functions & Architecture
Write a main function called process_courier_dispatch(request_batch, available_couriers).

Write a helper function called parse_distance(distance_string) to convert strings like "2.3km" or "850m" into a standardized float representing kilometers (km).

2. Control Flow
Before processing, sort the requests by tier. "premium" requests must be processed first, followed by "standard", and finally "economy".

Iterate through the sorted batch.

If a request targets a courier_id that is not in the available_couriers set, ignore the request completely and move to the next one.

3. Exceptions
Use try/except blocks to handle the following messy data scenarios:

Missing Keys: Some requests will be missing the order_id or distance keys. Catch this and flag the req_id as "invalid_schema".
Parsing Errors: If the distance string is malformed (for example, "nearby", a null value, or a distance over 15km), your helper function should throw a ValueError or TypeError. Catch this in the main loop and flag the req_id as "parsing_error".
Custom Exception: Define a CourierConflictError. As you process valid requests, keep track of which order each courier has been assigned to in this batch. A single courier can only carry one active order per batch window, so if a courier is scheduled for a second, different order, raise this exception, deny the dispatch, and flag the req_id as "courier_conflict".

4. Data Structures
Maintain a dictionary tracking the final assigned order for each courier (e.g., {"CR_15": "ORD_7001"}).

Return a final summary dictionary containing:

"dispatched_orders": An integer count of fully processed and dispatched requests.
"courier_orders": The dictionary of couriers and their assigned orders.
"failed_requests": A nested dictionary grouping failed req_ids by their error reason ("invalid_schema", "parsing_error", "courier_conflict").

Sample Test Data

json
{
  "available_couriers": ["CR_15", "CR_16", "CR_17", "CR_18", "CR_20"],
  "request_batch": [
    {"req_id": "D01", "order_id": "ORD_7001", "courier_id": "CR_15", "distance": "2.3km", "tier": "standard"},
    {"req_id": "D02", "order_id": "ORD_7002", "courier_id": "CR_99", "distance": "1.1km", "tier": "premium"},
    {"req_id": "D03", "order_id": "ORD_7003", "courier_id": "CR_16", "distance": "850m", "tier": "premium"},
    {"req_id": "D04", "order_id": "ORD_7004", "courier_id": "CR_17", "tier": "economy"},
    {"req_id": "D05", "order_id": "ORD_7005", "courier_id": "CR_18", "distance": "nearby", "tier": "standard"},
    {"req_id": "D06", "order_id": "ORD_7006", "courier_id": "CR_16", "distance": "4km", "tier": "premium"}
  ]
}