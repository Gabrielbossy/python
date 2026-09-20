The Problem: The Cloud Instance Firewall Provisioner

Background:
You are building an automated pipeline that applies firewall security group rules to a fleet of cloud compute instances. Different DevOps teams submit provisioning tasks asynchronously. Your script must process these requests, parse the string-based port ranges into usable integers, and prevent security group conflicts.

The Input:
You receive a list of task dictionaries and a Set of currently active instance IDs. A valid task looks like this:

python
{"task_id": "F01", "instance_id": "i-0a1b2c3d", "security_group": "sg-web", "port_range": "443/tcp", "tier": "production"}

The Requirements:

1. Functions & Architecture
Write a main function called process_firewall_configs(task_batch, active_instances).

Write a helper function called parse_port(port_string) to convert strings like "443/tcp" or "53/udp" into a standardized integer representing just the port number.

2. Control Flow
Before processing, sort the tasks by tier. "production" tasks must be processed first, followed by "staging", and finally "development".

Iterate through the sorted batch.

If a task targets an instance_id that does not exist in the active_instances set, ignore the task completely and move to the next one.

3. Exceptions
Use try/except blocks to handle the following messy data scenarios:

Missing Keys: Some tasks will be missing the security_group or port_range keys. Catch this and flag the task_id as "invalid_schema".
Parsing Errors: If the port string is malformed (for example, "Any", a null value, or a number outside 1–65535), your helper function should throw a ValueError or TypeError. Catch this in the main loop and flag the task_id as "parsing_error".
Custom Exception: Define a SecurityGroupConflictError. As you process valid tasks, keep track of which security groups are being assigned. A single security group can hold multiple instances, but a single instance cannot be assigned to two different security groups in the same batch. If an instance is scheduled for a second security group, raise this exception, deny the update, and flag the task_id as "sg_conflict".

4. Data Structures
Maintain a dictionary tracking the final assigned security group for each instance (e.g., {"i-0a1b2c3d": "sg-web"}).

Return a final summary dictionary containing:

"successful_updates": An integer count of fully applied tasks.
"instance_groups": The dictionary of instances and their newly assigned security groups.
"failed_tasks": A nested dictionary grouping failed task_ids by their error reason ("invalid_schema", "parsing_error", "sg_conflict").

Sample Test Data

json
{
  "active_instances": ["i-001", "i-002", "i-003", "i-004", "i-005"],
  "task_batch": [
    {"task_id": "F01", "instance_id": "i-001", "security_group": "sg-web", "port_range": "443/tcp", "tier": "staging"},
    {"task_id": "F02", "instance_id": "i-999", "security_group": "sg-db", "port_range": "5432/tcp", "tier": "production"},
    {"task_id": "F03", "instance_id": "i-002", "security_group": "sg-db", "port_range": "5432/tcp", "tier": "production"},
    {"task_id": "F04", "instance_id": "i-003", "security_group": "sg-web", "tier": "development"},
    {"task_id": "F05", "instance_id": "i-004", "security_group": "sg-cache", "port_range": "Any", "tier": "staging"},
    {"task_id": "F06", "instance_id": "i-002", "security_group": "sg-app", "port_range": "8080/tcp", "tier": "production"}
  ]
}