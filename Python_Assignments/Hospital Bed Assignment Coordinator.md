The Problem: The Hospital Bed Assignment Coordinator

Background:
You are building an automated pipeline for a hospital's admissions system that assigns incoming patients to available beds across different wards. Multiple intake desks submit assignment requests asynchronously throughout the day. Your script must process these requests, parse the string-based patient age into a usable integer, and prevent a patient from being double-assigned to two different wards.

The Input:
You receive a list of request dictionaries and a Set of ward names that currently have open beds. A valid request looks like this:

python
{"request_id": "P01", "patient_id": "PT_5001", "ward": "ICU", "age": "67", "condition": "critical"}

The Requirements:

1. Functions & Architecture
Write a main function called process_bed_assignments(request_batch, available_wards).

Write a helper function called parse_age(age_value) to convert values like "67" into a validated integer, ensuring it falls within a realistic human range of 0–120.

2. Control Flow
Before processing, sort the requests by condition. "critical" requests must be processed first, followed by "serious", and finally "stable".

Iterate through the sorted batch.

If a request targets a ward that is not in the available_wards set, ignore the request completely and move to the next one.

3. Exceptions
Use try/except blocks to handle the following messy data scenarios:

Missing Keys: Some requests will be missing the patient_id or age keys. Catch this and flag the request_id as "invalid_schema".
Parsing Errors: If the age value is malformed (for example, "unknown", a null value, or a number outside 0–120), your helper function should throw a ValueError or TypeError. Catch this in the main loop and flag the request_id as "parsing_error".
Custom Exception: Define a WardConflictError. As you process valid requests, keep track of which ward each patient has been assigned to in this batch. A single ward can hold multiple patients, but a single patient cannot be assigned to two different wards in the same batch. If a patient is scheduled for a second, different ward, raise this exception, deny the assignment, and flag the request_id as "ward_conflict".

4. Data Structures
Maintain a dictionary tracking the final assigned ward for each patient (e.g., {"PT_5001": "ICU"}).

Return a final summary dictionary containing:

"admitted_patients": An integer count of fully processed and admitted requests.
"patient_wards": The dictionary of patients and their assigned wards.
"failed_requests": A nested dictionary grouping failed request_ids by their error reason ("invalid_schema", "parsing_error", "ward_conflict").

Sample Test Data

json
{
  "available_wards": ["ICU", "Cardiology", "General", "Pediatrics", "Maternity"],
  "request_batch": [
    {"request_id": "P01", "patient_id": "PT_5001", "ward": "ICU", "age": "67", "condition": "serious"},
    {"request_id": "P02", "patient_id": "PT_5002", "ward": "Oncology", "age": "45", "condition": "critical"},
    {"request_id": "P03", "patient_id": "PT_5003", "ward": "ICU", "age": "34", "condition": "critical"},
    {"request_id": "P04", "patient_id": "PT_5004", "ward": "General", "condition": "stable"},
    {"request_id": "P05", "patient_id": "PT_5005", "ward": "Cardiology", "age": "unknown", "condition": "serious"},
    {"request_id": "P06", "patient_id": "PT_5003", "ward": "Cardiology", "age": "34", "condition": "critical"}
  ]
}