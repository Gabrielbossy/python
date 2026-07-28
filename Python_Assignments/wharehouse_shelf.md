The Warehouse Shelf Assignment

Background:
You're building a pipeline that assigns incoming inventory pallets to shelf 
zones in a warehouse. Multiple departments submit placement requests 
asynchronously. Your script must process these requests, parse the 
string-based weight capacities into usable integers, and prevent shelf 
zone conflicts.

The Input:
You receive a list of request dictionaries and a Set of currently active 
shelf zone IDs.
A valid request looks like this:
{"request_id": "R01", "pallet_id": "P-2201", "zone_id": "Z12", "max_weight": "500kg", "priority": "critical"}

The Requirements:

1. Functions & Architecture
Write a main function called process_shelf_assignments(request_batch, active_zones).

Write a helper function called parse_weight(weight_string) to convert 
strings like "500kg" or "2ton" into a standardized integer representing 
kilograms (kg). Assume 1 ton = 1000kg.

2. Control Flow
Before processing, sort the requests by priority. "critical" requests must 
be processed first, followed by "standard", and finally "backlog".

Iterate through the sorted batch.

If a request targets a zone_id that does not exist in the active_zones 
set, ignore the request completely and move to the next one.

3. Exceptions
Use try/except blocks to handle the following messy data scenarios:

Missing Keys: Some requests will be missing the pallet_id or max_weight 
keys. Catch this and flag the request_id as "invalid_schema".

Parsing Errors: If the weight string is malformed (for example, "Full" or 
a null value), your helper function should throw a ValueError or 
TypeError. Catch this in the main loop and flag the request_id as 
"parsing_error".

Custom Exception: Define a PalletConflictError. As you process valid 
requests, keep track of which zone each pallet is being assigned to. A 
single zone can hold multiple pallets, but a single pallet cannot be 
assigned to two different zones in the same batch. If a pallet is 
scheduled for a second zone, raise this exception, deny the update, and 
flag the request_id as "pallet_conflict".

4. Data Structures
Maintain a dictionary tracking the final assigned zone for each pallet 
(e.g., {"P-2201": "Z12"}).

Return a final summary dictionary containing:

"successful_placements": An integer count of fully applied requests.

"pallet_zones": The dictionary of pallets and their newly assigned zones.

"failed_requests": A nested dictionary grouping failed request_ids by 
their error reason ("invalid_schema", "parsing_error", "pallet_conflict").

Sample Test Data

{
  "active_zones": ["Z12", "Z13", "Z14", "Z15", "Z20"],
  "request_batch": [
    {"request_id": "R01", "pallet_id": "P-2201", "zone_id": "Z12", "max_weight": "500kg", "priority": "standard"},
    {"request_id": "R02", "pallet_id": "P-9999", "zone_id": "Z99", "max_weight": "100kg", "priority": "critical"},
    {"request_id": "R03", "pallet_id": "P-2202", "zone_id": "Z13", "max_weight": "1ton", "priority": "critical"},
    {"request_id": "R04", "pallet_id": "P-2203", "zone_id": "Z14", "priority": "backlog"},
    {"request_id": "R05", "pallet_id": "P-2204", "zone_id": "Z15", "max_weight": "Full", "priority": "standard"},
    {"request_id": "R06", "pallet_id": "P-2202", "zone_id": "Z20", "max_weight": "200kg", "priority": "critical"}
  ]
}