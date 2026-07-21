The Problem: The Unreliable Sensor Network
Background:
You are building an aggregation pipeline for a network of city traffic sensors. The sensors send hourly heartbeat logs to a central server, but the data stream is highly unreliable.

The Input:
You receive a list of raw log dictionaries. A perfectly formatted log looks like this:
{"sensor_id": "A1", "zone": "North_Gate", "vehicle_count": 450, "status": "active"}

However, the incoming batch contains malformed data, missing fields, corrupted types, and offline sensors.

The Requirements:

1. Functions & Architecture
Write a main entry-point function called process_sensor_batch(batch_data).

Write at least one separate helper function, validate_and_extract(log), to handle the validation of individual log entries.

2. Control Flow
Iterate through the batch of logs.

Ignore any log where the status is explicitly set to "offline" or "maintenance".

Keep a running tally of how many logs were successfully processed versus how many failed validation.

3. Exceptions
Your code must anticipate and handle the following bad data scenarios using explicit try/except blocks:

Missing Keys: Some dictionaries will be missing the zone or vehicle_count keys. Catch this (e.g., KeyError in Python) and record the sensor_id as "failed".

Corrupted Data Types: Sometimes vehicle_count comes in as a string like "ERR_TIMEOUT" instead of an integer. Catch the resulting type/value error when attempting to process it.

Custom Exception: Define a custom exception called NegativeCountError. Raise this if a sensor reports a vehicle_count less than zero. Catch it in your main loop and flag that specific sensor as "calibrating".

4. Data Structures
Aggregate the valid data into a nested dictionary structured like this:
{ "Zone_Name": [count1, count2, count3] }

Once the batch is processed, return a final summary dictionary containing:

"zone_averages": A dictionary mapping each zone to its average vehicle count (rounded to 2 decimal places).

"failed_sensors": A Set containing the unique sensor_ids of any sensor that threw an exception during processing.

"total_processed": The integer count of fully valid logs.

Sample Test Data
You can provide this payload for the candidate to test their code against:

JSON
[
  {"sensor_id": "S01", "zone": "CBD", "vehicle_count": 120, "status": "active"},
  {"sensor_id": "S02", "zone": "CBD", "vehicle_count": "N/A", "status": "active"},
  {"sensor_id": "S03", "zone": "Westlands", "vehicle_count": 45, "status": "active"},
  {"sensor_id": "S04", "zone": "Eastleigh", "status": "active"}, 
  {"sensor_id": "S05", "zone": "CBD", "vehicle_count": -15, "status": "active"},
  {"sensor_id": "S06", "zone": "Westlands", "vehicle_count": 80, "status": "maintenance"},
  {"sensor_id": "S07", "zone": "Eastleigh", "vehicle_count": 310, "status": "active"}
]