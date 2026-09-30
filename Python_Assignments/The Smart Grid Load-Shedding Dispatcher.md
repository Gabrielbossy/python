The Problem: The Smart Grid Load-Shedding Dispatcher

Background:
You are building an automated pipeline for a regional power utility that sheds electrical load across substations during peak demand events. Different grid control centers submit shedding requests asynchronously throughout the event. Your script must process these requests, parse the string-based load values into usable floats, and prevent a substation from being shed under two conflicting outage tickets.

The Input:
You receive a list of request dictionaries and a Set of substation IDs currently online and eligible for shedding. A valid request looks like this:

python
{"req_id": "G01", "substation_id": "SUB_204", "outage_ticket": "OUT-8001", "load_kw": "450.5kW", "tier": "emergency"}

The Requirements:

1. Functions & Architecture
Write a main function called process_load_shedding(request_batch, online_substations).

Write a helper function called parse_load(load_string) to convert strings like "450.5kW" or "1.2MW" into a standardized float representing kilowatts (kW).

2. Control Flow
Before processing, sort the requests by tier. "emergency" requests must be processed first, followed by "scheduled", and finally "voluntary".

Iterate through the sorted batch.

If a request targets a substation_id that is not in the online_substations set, ignore the request completely and move to the next one.

3. Exceptions
Use try/except blocks to handle the following messy data scenarios:

Missing Keys: Some requests will be missing the outage_ticket or load_kw keys. Catch this and flag the req_id as "invalid_schema".
Parsing Errors: If the load string is malformed (for example, "TBD", a null value, or a negative number), your helper function should throw a ValueError or TypeError. Catch this in the main loop and flag the req_id as "parsing_error".
Custom Exception: Define an OutageTicketConflictError. As you process valid requests, keep track of which outage ticket each substation has been assigned to in this batch. A single ticket can cover multiple substations, but a single substation cannot be linked to two different tickets in the same batch. If a substation is scheduled under a second, different ticket, raise this exception, deny the shed, and flag the req_id as "ticket_conflict".

4. Data Structures
Maintain a dictionary tracking the final assigned outage ticket for each substation (e.g., {"SUB_204": "OUT-8001"}).

Return a final summary dictionary containing:

"shed_substations": An integer count of fully processed and shed requests.
"substation_tickets": The dictionary of substations and their assigned outage tickets.
"failed_requests": A nested dictionary grouping failed req_ids by their error reason ("invalid_schema", "parsing_error", "ticket_conflict").

Sample Test Data

json
{
  "online_substations": ["SUB_204", "SUB_205", "SUB_206", "SUB_207", "SUB_300"],
  "request_batch": [
    {"req_id": "G01", "substation_id": "SUB_204", "outage_ticket": "OUT-8001", "load_kw": "450.5kW", "tier": "scheduled"},
    {"req_id": "G02", "substation_id": "SUB_999", "outage_ticket": "OUT-8002", "load_kw": "300kW", "tier": "emergency"},
    {"req_id": "G03", "substation_id": "SUB_205", "outage_ticket": "OUT-8003", "load_kw": "1.2MW", "tier": "emergency"},
    {"req_id": "G04", "substation_id": "SUB_206", "load_kw": "200kW", "tier": "voluntary"},
    {"req_id": "G05", "substation_id": "SUB_207", "outage_ticket": "OUT-8004", "load_kw": "TBD", "tier": "scheduled"},
    {"req_id": "G06", "substation_id": "SUB_205", "outage_ticket": "OUT-8005", "load_kw": "800kW", "tier": "emergency"}
  ]
}