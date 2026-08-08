The Hospital Bed Assignment System

Background:
You're building a pipeline that assigns incoming patients to hospital ward 
beds. Requests are submitted asynchronously by different intake stations. 
Your script must process these requests, parse the string-based stay 
durations into usable integers, and prevent ward conflicts for the same 
patient.

The Input:
You receive a list of admission dictionaries and a Set of currently active 
ward IDs.
A valid admission looks like this:
{"request_id": "H01", "patient_id": "P-3001", "ward_id": "W04", "stay_duration": "3days", "severity": "emergency"}

The Requirements:

1. Functions & Architecture
Write a main function called process_bed_assignments(admission_batch, active_wards).

Write a helper function called parse_stay_duration(duration_string) to 
convert strings like "3days" or "12hrs" into a standardized integer 
representing hours. Assume 1 day = 24hrs.

2. Control Flow
Before processing, sort the admissions by severity. "emergency" admissions 
must be processed first, followed by "urgent", and finally "routine".

Iterate through the sorted batch.

If an admission targets a ward_id that does not exist in the active_wards 
set, ignore the admission completely and move to the next one.

3. Exceptions
Use try/except blocks to handle the following messy data scenarios:

Missing Keys: Some admissions will be missing the patient_id or 
stay_duration keys. Catch this and flag the request_id as "invalid_schema".

Parsing Errors: If the duration string is malformed (for example, 
"Unknown" or a null value), your helper function should throw a 
ValueError or TypeError. Catch this in the main loop and flag the 
request_id as "parsing_error".

Custom Exception: Define a WardConflictError. As you process valid 
admissions, keep track of which ward each patient is being assigned to. A 
single ward can hold multiple patients, but a single patient cannot be 
assigned to two different wards in the same batch. If a patient is 
scheduled for a second ward, raise this exception, deny the update, and 
flag the request_id as "ward_conflict".

4. Data Structures
Maintain a dictionary tracking the final assigned ward for each patient 
(e.g., {"P-3001": "W04"}).

Return a final summary dictionary containing:

"successful_admissions": An integer count of fully applied admissions.

"patient_wards": The dictionary of patients and their newly assigned wards.

"failed_admissions": A nested dictionary grouping failed request_ids by 
their error reason ("invalid_schema", "parsing_error", "ward_conflict").

Sample Test Data

{
  "active_wards": ["W01", "W02", "W03", "W04", "W07"],
  "admission_batch": [
    {"request_id": "H01", "patient_id": "P-3001", "ward_id": "W04", "stay_duration": "3days", "severity": "urgent"},
    {"request_id": "H02", "patient_id": "P-3009", "ward_id": "W99", "stay_duration": "12hrs", "severity": "emergency"},
    {"request_id": "H03", "patient_id": "P-3002", "ward_id": "W01", "stay_duration": "48hrs", "severity": "emergency"},
    {"request_id": "H04", "patient_id": "P-3003", "ward_id": "W02", "severity": "routine"},
    {"request_id": "H05", "patient_id": "P-3004", "ward_id": "W07", "stay_duration": "Unknown", "severity": "urgent"},
    {"request_id": "H06", "patient_id": "P-3002", "ward_id": "W03", "stay_duration": "6hrs", "severity": "emergency"}
  ]
}