The Fleet Network Rollout
Background:
You are building an automated pipeline that applies network configurations (like Netplan routing profiles) to a fleet of Linux servers. Different development teams submit configuration tasks asynchronously. Your script must process these requests, parse the string-based bandwidth limits into usable integers, and prevent network conflicts.

The Input:
You receive a list of task dictionaries and a Set of currently active server IP addresses.
A valid task looks like this:
{"task_id": "T01", "server_ip": "10.0.0.5", "vlan_id": 40, "bandwidth": "500Mbps", "env": "production"}

The Requirements:

1. Functions & Architecture
Write a main function called process_network_configs(task_batch, active_servers).

Write a helper function called parse_bandwidth(bw_string) to convert strings like "500Mbps" or "1Gbps" into a standardized integer representing Megabits per second (Mbps).

2. Control Flow
Before processing, sort the tasks by environment. "production" tasks must be processed first, followed by "staging", and finally "development".

Iterate through the sorted batch.

If a task targets a server_ip that does not exist in the active_servers set, ignore the task completely and move to the next one.

3. Exceptions
Use try/except blocks to handle the following messy data scenarios:

Missing Keys: Some tasks will be missing the vlan_id or bandwidth keys. Catch this and flag the task_id as "invalid_schema".

Parsing Errors: If the bandwidth string is malformed (for example, "Unlimited" or a null value), your helper function should throw a ValueError or TypeError. Catch this in the main loop and flag the task_id as "parsing_error".

Custom Exception: Define a VlanConflictError. As you process valid tasks, keep track of which VLANs are being assigned. A single VLAN can hold multiple servers, but a single server cannot be assigned to two different VLANs in the same batch. If a server is scheduled for a second VLAN, raise this exception, deny the update, and flag the task_id as "vlan_conflict".

4. Data Structures
Maintain a dictionary tracking the final assigned VLAN for each server (e.g., {"10.0.0.5": 40}).

Return a final summary dictionary containing:

"successful_updates": An integer count of fully applied tasks.

"server_vlans": The dictionary of servers and their newly assigned VLANs.

"failed_tasks": A nested dictionary grouping failed task_ids by their error reason ("invalid_schema", "parsing_error", "vlan_conflict").

Sample Test Data
Here is the JSON payload to test the script:

JSON
{
  "active_servers": ["10.0.0.5", "10.0.0.6", "10.0.0.7", "10.0.0.8", "10.0.1.10"],
  "task_batch": [
    {"task_id": "T01", "server_ip": "10.0.0.5", "vlan_id": 40, "bandwidth": "500Mbps", "env": "staging"},
    {"task_id": "T02", "server_ip": "10.0.1.99", "vlan_id": 20, "bandwidth": "100Mbps", "env": "production"},
    {"task_id": "T03", "server_ip": "10.0.0.6", "vlan_id": 10, "bandwidth": "1Gbps", "env": "production"},
    {"task_id": "T04", "server_ip": "10.0.0.7", "vlan_id": 40, "env": "development"},
    {"task_id": "T05", "server_ip": "10.0.0.8", "vlan_id": 30, "bandwidth": "Max", "env": "staging"},
    {"task_id": "T06", "server_ip": "10.0.0.6", "vlan_id": 50, "bandwidth": "200Mbps", "env": "production"}
  ]
}