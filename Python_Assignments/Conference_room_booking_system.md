The Conference Room Booking System

Background:
You're building a pipeline that processes conference room booking requests 
submitted by employees across the company. Bookings arrive asynchronously 
from different departments. Your script must process these requests, parse 
the string-based meeting durations into usable integers, and prevent 
double-booking conflicts for the same employee.

The Input:
You receive a list of booking dictionaries and a Set of currently active 
room IDs.
A valid booking looks like this:
{"booking_id": "B01", "employee_id": "E-101", "room_id": "R05", "duration": "60min", "tier": "executive"}

The Requirements:

1. Functions & Architecture
Write a main function called process_room_bookings(booking_batch, active_rooms).

Write a helper function called parse_duration(duration_string) to convert 
strings like "60min" or "2hr" into a standardized integer representing 
minutes. Assume 1 hr = 60min.

2. Control Flow
Before processing, sort the bookings by tier. "executive" bookings must be 
processed first, followed by "team", and finally "personal".

Iterate through the sorted batch.

If a booking targets a room_id that does not exist in the active_rooms 
set, ignore the booking completely and move to the next one.

3. Exceptions
Use try/except blocks to handle the following messy data scenarios:

Missing Keys: Some bookings will be missing the employee_id or duration 
keys. Catch this and flag the booking_id as "invalid_schema".

Parsing Errors: If the duration string is malformed (for example, "TBD" 
or a null value), your helper function should throw a ValueError or 
TypeError. Catch this in the main loop and flag the booking_id as 
"parsing_error".

Custom Exception: Define a RoomConflictError. As you process valid 
bookings, keep track of which room each employee is being assigned to. A 
single room can hold multiple employees (e.g. a shared meeting), but a 
single employee cannot be assigned to two different rooms in the same 
batch. If an employee is scheduled for a second room, raise this 
exception, deny the update, and flag the booking_id as "room_conflict".

4. Data Structures
Maintain a dictionary tracking the final assigned room for each employee 
(e.g., {"E-101": "R05"}).

Return a final summary dictionary containing:

"successful_bookings": An integer count of fully applied bookings.

"employee_rooms": The dictionary of employees and their newly assigned rooms.

"failed_bookings": A nested dictionary grouping failed booking_ids by 
their error reason ("invalid_schema", "parsing_error", "room_conflict").

Sample Test Data

{
  "active_rooms": ["R01", "R02", "R03", "R05", "R08"],
  "booking_batch": [
    {"booking_id": "B01", "employee_id": "E-101", "room_id": "R05", "duration": "60min", "tier": "team"},
    {"booking_id": "B02", "employee_id": "E-909", "room_id": "R99", "duration": "30min", "tier": "executive"},
    {"booking_id": "B03", "employee_id": "E-102", "room_id": "R01", "duration": "2hr", "tier": "executive"},
    {"booking_id": "B04", "employee_id": "E-103", "room_id": "R02", "tier": "personal"},
    {"booking_id": "B05", "employee_id": "E-104", "room_id": "R08", "duration": "TBD", "tier": "team"},
    {"booking_id": "B06", "employee_id": "E-102", "room_id": "R03", "duration": "45min", "tier": "executive"}
  ]
}