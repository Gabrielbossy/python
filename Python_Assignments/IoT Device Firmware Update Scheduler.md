The Problem: The IoT Device Firmware Update Scheduler

Background:
You are building an automated pipeline that pushes firmware updates to a fleet of IoT devices deployed across a smart building. Different maintenance teams submit update jobs asynchronously. Your script must process these requests, parse the string-based firmware version numbers into comparable values, and prevent devices from being flashed twice in the same batch.

The Input:
You receive a list of job dictionaries and a Set of currently online device IDs. A valid job looks like this:

python
{"job_id": "J01", "device_id": "DEV_1001", "zone": "floor3", "firmware_version": "v2.4.1", "priority": "critical"}

The Requirements:

1. Functions & Architecture
Write a main function called process_firmware_updates(job_batch, online_devices).

Write a helper function called parse_version(version_string) to convert strings like "v2.4.1" or "v3.0" into a standardized tuple of integers, e.g. (2, 4, 1) or (3, 0, 0), for easy comparison.

2. Control Flow
Before processing, sort the jobs by priority. "critical" jobs must be processed first, followed by "routine", and finally "optional".

Iterate through the sorted batch.

If a job targets a device_id that does not exist in the online_devices set, ignore the job completely and move to the next one.

3. Exceptions
Use try/except blocks to handle the following messy data scenarios:

Missing Keys: Some jobs will be missing the zone or firmware_version keys. Catch this and flag the job_id as "invalid_schema".
Parsing Errors: If the version string is malformed (for example, "latest", a null value, or doesn't start with "v"), your helper function should throw a ValueError or TypeError. Catch this in the main loop and flag the job_id as "parsing_error".
Custom Exception: Define a DeviceFlashConflictError. As you process valid jobs, keep track of which devices have already been flashed in this batch. A single zone can have multiple devices updated, but a single device cannot be flashed with two different firmware versions in the same batch. If a device is scheduled for a second, different version, raise this exception, deny the update, and flag the job_id as "flash_conflict".

4. Data Structures
Maintain a dictionary tracking the final applied firmware version for each device (e.g., {"DEV_1001": "v2.4.1"}).

Return a final summary dictionary containing:

"successful_updates": An integer count of fully applied jobs.
"device_firmware": The dictionary of devices and their newly applied firmware versions.
"failed_jobs": A nested dictionary grouping failed job_ids by their error reason ("invalid_schema", "parsing_error", "flash_conflict").

Sample Test Data

json
{
  "online_devices": ["DEV_1001", "DEV_1002", "DEV_1003", "DEV_1004", "DEV_1005"],
  "job_batch": [
    {"job_id": "J01", "device_id": "DEV_1001", "zone": "floor3", "firmware_version": "v2.4.1", "priority": "routine"},
    {"job_id": "J02", "device_id": "DEV_9999", "zone": "floor1", "firmware_version": "v1.0.0", "priority": "critical"},
    {"job_id": "J03", "device_id": "DEV_1002", "zone": "floor1", "firmware_version": "v3.2.0", "priority": "critical"},
    {"job_id": "J04", "device_id": "DEV_1003", "firmware_version": "v1.5.0", "priority": "optional"},
    {"job_id": "J05", "device_id": "DEV_1004", "zone": "floor2", "firmware_version": "latest", "priority": "routine"},
    {"job_id": "J06", "device_id": "DEV_1002", "zone": "floor1", "firmware_version": "v3.3.0", "priority": "critical"}
  ]
}