The Problem: The Conference Room Reservation Engine

Background:
You are building the backend reservation processor for a corporate campus's meeting room system. Employees submit booking requests throughout the day, and your script processes them in batches before the room schedules lock for the day.

Each meeting room has a strict maximum number of bookable minutes remaining today. Your system must allocate rooms fairly while filtering out bad data and preventing employees from double-booking themselves into overlapping meetings.

The Input:
You receive a list of dictionary requests and a dictionary representing the total available minutes for each room today.

A perfect request looks like this:

python
{"req_id": "M01", "employee_id": "EMP_400", "room": "Boardroom_1", "minutes": 30, "level": "executive"}

The Requirements:

1. Functions & Architecture
Write a main entry-point function called process_room_reservations(reservation_batch, room_availability).

Write a helper function called parse_minutes(minutes_value) to isolate the validation of the requested meeting length.

2. Control Flow
Before looping through the batch, sort the requests by level: "executive" requests must be processed before "team", and "team" before "individual".

Iterate through the sorted batch.

If a valid request asks for more minutes than the room currently has left, deny the reservation but continue processing the rest of the queue. Deduct the minutes from room_availability only if the reservation is approved.

3. Exceptions
Anticipate and handle these failure modes using explicit try/except blocks:

Missing Keys: Some dictionaries will be missing the room or minutes keys. Catch this and flag the req_id as a "data_error".
Invalid Types: Sometimes minutes is a string like "half an hour" or a null value, or a negative/zero number, or exceeds 240 (the max single-meeting length). Catch the resulting ValueError or TypeError in your helper function and raise it to be caught by the main loop.
Custom Exception: Define OverlappingBookingError. Track which employee_ids have already successfully reserved a room in this batch. If an employee tries to reserve a second room, raise this exception and flag the req_id as a "policy_violation".

4. Data Structures
Maintain a Set of employee_ids to track who has already secured a room.

Return a final summary dictionary containing:

"confirmed_reservations": A List of the req_ids that were successfully booked.
"denied_availability": A List of req_ids denied because the room ran out of available minutes.
"failed_requests": A Dictionary mapping the error type ("data_error" or "policy_violation") to a List of the corresponding req_ids.
"remaining_availability": The updated room_availability dictionary.

Sample Test Data

json
{
  "room_availability": {
    "Boardroom_1": 90,
    "Huddle_2": 120
  },
  "reservation_batch": [
    {"req_id": "M01", "employee_id": "EMP_01", "room": "Boardroom_1", "minutes": 60, "level": "team"},
    {"req_id": "M02", "employee_id": "EMP_02", "room": "Huddle_2", "minutes": "half an hour", "level": "executive"},
    {"req_id": "M03", "employee_id": "EMP_03", "minutes": 45, "level": "team"},
    {"req_id": "M04", "employee_id": "EMP_01", "room": "Huddle_2", "minutes": 30, "level": "individual"},
    {"req_id": "M05", "employee_id": "EMP_05", "room": "Boardroom_1", "minutes": 45, "level": "executive"},
    {"req_id": "M06", "employee_id": "EMP_06", "room": "Huddle_2", "minutes": 300, "level": "team"}
  ]
}