The Airline Gate Assignment System

Background:
You're building a pipeline that assigns incoming flights to airport gates. 
Requests come in asynchronously from different terminal operations teams. 
Your script must process these requests, parse the string-based fuel load 
values into usable integers, and prevent gate conflicts for the same 
flight.

The Input:
You receive a list of assignment dictionaries and a Set of currently 
active gate IDs.
A valid assignment looks like this:
{"assignment_id": "G01", "flight_id": "FL-220", "gate_id": "A5", "fuel_load": "5000L", "flight_type": "international"}

The Requirements:

1. Functions & Architecture
Write a main function called process_gate_assignments(assignment_batch, active_gates).

Write a helper function called parse_fuel_load(fuel_string) to convert 
strings like "5000L" or "5kL" into a standardized integer representing 
liters (L). Assume 1 kL = 1000L.

2. Control Flow
Before processing, sort the assignments by flight_type. "international" 
assignments must be processed first, followed by "domestic", and finally 
"regional".

Iterate through the sorted batch.

If an assignment targets a gate_id that does not exist in the 
active_gates set, ignore the assignment completely and move to the next 
one.

3. Exceptions
Use try/except blocks to handle the following messy data scenarios:

Missing Keys: Some assignments will be missing the flight_id or fuel_load 
keys. Catch this and flag the assignment_id as "invalid_schema".

Parsing Errors: If the fuel load string is malformed (for example, "Full" 
or a null value), your helper function should throw a ValueError or 
TypeError. Catch this in the main loop and flag the assignment_id as 
"parsing_error".

Custom Exception: Define a GateConflictError. As you process valid 
assignments, keep track of which gate each flight is being assigned to. A 
single gate can be reused across multiple assignments for the same 
flight, but a single flight cannot be assigned to two different gates in 
the same batch. If a flight is scheduled for a second gate, raise this 
exception, deny the update, and flag the assignment_id as "gate_conflict".

4. Data Structures
Maintain a dictionary tracking the final assigned gate for each flight 
(e.g., {"FL-220": "A5"}).

Return a final summary dictionary containing:

"successful_assignments": An integer count of fully applied assignments.

"flight_gates": The dictionary of flights and their newly assigned gates.

"failed_assignments": A nested dictionary grouping failed assignment_ids 
by their error reason ("invalid_schema", "parsing_error", "gate_conflict").

Sample Test Data

{
  "active_gates": ["A1", "A2", "A5", "B3", "B7"],
  "assignment_batch": [