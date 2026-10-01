The Problem: The Airline Gate Assignment System

Background:
You are building an automated pipeline for an airport operations center that assigns arriving flights to terminal gates. Different airline control desks submit gate requests asynchronously throughout the day. Your script must process these requests, parse the string-based turnaround time into usable integers, and prevent a flight from being assigned to two conflicting gates.

The Input:
You receive a list of request dictionaries and a Set of gate IDs currently free for assignment. A valid request looks like this:

python
{"req_id": "GA01", "flight_id": "FL_2201", "gate": "B12", "turnaround": "45min", "class": "international"}

The Requirements:

1. Functions & Architecture
Write a main function called process_gate_assignments(request_batch, free_gates).

Write a helper function called parse_turnaround(turnaround_string) to convert strings like "45min" or "1hr" into a standardized integer representing minutes.

2. Control Flow
Before processing, sort the requests by class. "international" requests must be processed first, followed by "domestic", and finally "cargo".

Iterate through the sorted batch.

If a request targets a gate that is not in the free_gates set, ignore the request completely and move to the next one.

3. Exceptions
Use try/except blocks to handle the following messy data scenarios:

Missing Keys: Some requests will be missing the flight_id or turnaround keys. Catch this and flag the req_id as "invalid_schema".
Parsing Errors: If the turnaround string is malformed (for example, "soon", a null value, or a value over 180 minutes), your helper function should throw a ValueError or TypeError. Catch this in the main loop and flag the req_id as "parsing_error".
Custom Exception: Define a GateConflictError. As you process valid requests, keep track of which gate each flight has been assigned to in this batch. A single gate can serve multiple flights sequentially, but a single flight cannot be assigned to two different gates in the same batch. If a flight is scheduled for a second, different gate, raise this exception, deny the assignment, and flag the req_id as "gate_conflict".

4. Data Structures
Maintain a dictionary tracking the final assigned gate for each flight (e.g., {"FL_2201": "B12"}).

Return a final summary dictionary containing:

"assigned_flights": An integer count of fully processed and assigned requests.
"flight_gates": The dictionary of flights and their assigned gates.
"failed_requests": A nested dictionary grouping failed req_ids by their error reason ("invalid_schema", "parsing_error", "gate_conflict").

Sample Test Data

json
{
  "free_gates": ["B12", "B13", "C04", "C05", "A01"],
  "request_batch": [
    {"req_id": "GA01", "flight_id": "FL_2201", "gate": "B12", "turnaround": "45min", "class": "domestic"},
    {"req_id": "GA02", "flight_id": "FL_2202", "gate": "D99", "turnaround": "30min", "class": "international"},
    {"req_id": "GA03", "flight_id": "FL_2203", "gate": "C04", "turnaround": "1hr", "class": "international"},
    {"req_id": "GA04", "flight_id": "FL_2204", "gate": "A01", "class": "cargo"},
    {"req_id": "GA05", "flight_id": "FL_2205", "gate": "B13", "turnaround": "soon", "class": "domestic"},
    {"req_id": "GA06", "flight_id": "FL_2203", "gate": "B12", "turnaround": "50min", "class": "international"}
  ]
}