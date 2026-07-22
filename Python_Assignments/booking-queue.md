
The Problem: The Lab Booking Queue
Background:
You are building the backend queue processor for a university laboratory scheduling system. Students submit booking requests throughout the day, and your script processes them in batches.

Labs have a strict maximum daily capacity in minutes. Your system must allocate time fairly while filtering out bad data and preventing greedy students from double-booking.

The Input:
You receive a list of dictionary requests and a dictionary representing the total available minutes for each lab today.
A perfect request looks like this:
{"req_id": "R01", "student_id": "STU_100", "lab": "Software_Lab", "duration": 120, "priority": "high"}

The Requirements:

1. Functions & Architecture
Write a main entry-point function called process_lab_bookings(booking_batch, lab_capacities).

Write a helper function called parse_duration(duration_value) to isolate the validation of the time requested.

2. Control Flow
Before looping through the batch, sort the requests by priority: "high" priority requests must be processed before "normal" priority, and "normal" before "low".

Iterate through the sorted batch.

If a valid request asks for more time than the lab currently has left, deny the booking but continue processing the rest of the queue. Deduct the time from lab_capacities only if the booking is approved.

3. Exceptions
Anticipate and handle these failure modes using explicit try/except blocks:

Missing Keys: Some dictionaries will be missing the lab or duration keys. Catch this and flag the req_id as a "data_error".

Invalid Types: Sometimes duration is a string like "two hours" or a null value. Catch the resulting ValueError or TypeError in your helper function and raise it to be caught by the main loop.

Custom Exception: Define DoubleBookingError. Track which student_ids have already successfully booked a lab in this batch. If a student tries to book a second time, raise this exception and flag the req_id as a "policy_violation".

4. Data Structures
Maintain a Set of student_ids to track who has already secured a booking.

Return a final summary dictionary containing:

"approved_bookings": A List of the req_ids that were successfully scheduled.

"denied_capacity": A List of req_ids denied because the lab ran out of time.

"failed_requests": A Dictionary mapping the error type ("data_error" or "policy_violation") to a List of the corresponding req_ids.

"remaining_capacities": The updated lab_capacities dictionary.

Sample Test Data
Here is the payload to test the logic:

JSON
{
  "lab_capacities": {
    "Network_Lab": 300,
    "Software_Lab": 200
  },
  "booking_batch": [
    {"req_id": "B01", "student_id": "EDU_01", "lab": "Network_Lab", "duration": 120, "priority": "normal"},
    {"req_id": "B02", "student_id": "EDU_02", "lab": "Software_Lab", "duration": "invalid_string", "priority": "high"},
    {"req_id": "B03", "student_id": "EDU_03", "duration": 60, "priority": "normal"},
    {"req_id": "B04", "student_id": "EDU_01", "lab": "Software_Lab", "duration": 90, "priority": "low"},
    {"req_id": "B05", "student_id": "EDU_05", "lab": "Network_Lab", "duration": 200, "priority": "high"},
    {"req_id": "B06", "student_id": "EDU_06", "lab": "Network_Lab", "duration": 60, "priority": "normal"}
  ]
}