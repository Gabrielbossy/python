The Cluster Job Scheduler

Background:
You're building a pipeline that schedules incoming compute jobs onto nodes 
in a server cluster. Different teams submit job requests asynchronously. 
Your script must process these requests, parse the string-based memory 
requirements into usable integers, and prevent node conflicts.

The Input:
You receive a list of job dictionaries and a Set of currently active node IDs.
A valid job looks like this:
{"job_id": "J01", "task_id": "T-501", "node_id": "N03", "memory": "512MB", "urgency": "urgent"}

The Requirements:

1. Functions & Architecture
Write a main function called process_job_schedule(job_batch, active_nodes).

Write a helper function called parse_memory(mem_string) to convert strings 
like "512MB" or "2GB" into a standardized integer representing Megabytes 
(MB). Assume 1 GB = 1024MB.

2. Control Flow
Before processing, sort the jobs by urgency. "urgent" jobs must be 
processed first, followed by "normal", and finally "low".

Iterate through the sorted batch.

If a job targets a node_id that does not exist in the active_nodes set, 
ignore the job completely and move to the next one.

3. Exceptions
Use try/except blocks to handle the following messy data scenarios:

Missing Keys: Some jobs will be missing the task_id or memory keys. Catch 
this and flag the job_id as "invalid_schema".

Parsing Errors: If the memory string is malformed (for example, "Auto" or 
a null value), your helper function should throw a ValueError or 
TypeError. Catch this in the main loop and flag the job_id as 
"parsing_error".

Custom Exception: Define a NodeConflictError. As you process valid jobs, 
keep track of which node each task is being assigned to. A single node 
can hold multiple tasks, but a single task cannot be assigned to two 
different nodes in the same batch. If a task is scheduled for a second 
node, raise this exception, deny the update, and flag the job_id as 
"node_conflict".

4. Data Structures
Maintain a dictionary tracking the final assigned node for each task 
(e.g., {"T-501": "N03"}).

Return a final summary dictionary containing:

"successful_schedules": An integer count of fully applied jobs.

"task_nodes": The dictionary of tasks and their newly assigned nodes.

"failed_jobs": A nested dictionary grouping failed job_ids by their error 
reason ("invalid_schema", "parsing_error", "node_conflict").

Sample Test Data

{
  "active_nodes": ["N01", "N02", "N03", "N04", "N10"],
  "job_batch": [
    {"job_id": "J01", "task_id": "T-501", "node_id": "N03", "memory": "512MB", "urgency": "normal"},
    {"job_id": "J02", "task_id": "T-777", "node_id": "N99", "memory": "256MB", "urgency": "urgent"},
    {"job_id": "J03", "task_id": "T-502", "node_id": "N01", "memory": "2GB", "urgency": "urgent"},
    {"job_id": "J04", "task_id": "T-503", "node_id": "N02", "urgency": "low"},
    {"job_id": "J05", "task_id": "T-504", "node_id": "N04", "memory": "Auto", "urgency": "normal"},
    {"job_id": "J06", "task_id": "T-502", "node_id": "N10", "memory": "128MB", "urgency": "urgent"}
  ]
}