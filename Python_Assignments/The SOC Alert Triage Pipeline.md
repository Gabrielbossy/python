The Problem: The SOC Alert Triage Pipeline

Background:
You are building an automated pipeline for a Security Operations Center (SOC) that triages incoming intrusion detection alerts before they reach human analysts. Different sensor feeds submit alerts asynchronously throughout the day. Your script must process these alerts, parse the string-based CVSS severity scores into usable floats, and prevent the same host from being escalated under two conflicting incident tickets.

The Input:
You receive a list of alert dictionaries and a Set of currently monitored host IPs. A valid alert looks like this:

python
{"alert_id": "A01", "host_ip": "192.168.1.15", "ticket_id": "INC-4001", "cvss_score": "7.5", "severity": "high"}

The Requirements:

1. Functions & Architecture
Write a main function called process_soc_alerts(alert_batch, monitored_hosts).

Write a helper function called parse_cvss(cvss_string) to convert strings like "7.5" or "9.8" into a standardized float, validated to fall within the real CVSS range of 0.0–10.0.

2. Control Flow
Before processing, sort the alerts by severity. "critical" alerts must be processed first, followed by "high", and finally "medium".

Iterate through the sorted batch.

If an alert targets a host_ip that does not exist in the monitored_hosts set, ignore the alert completely and move to the next one.

3. Exceptions
Use try/except blocks to handle the following messy data scenarios:

Missing Keys: Some alerts will be missing the ticket_id or cvss_score keys. Catch this and flag the alert_id as "invalid_schema".
Parsing Errors: If the CVSS score string is malformed (for example, "N/A", a null value, or a number outside 0.0–10.0), your helper function should throw a ValueError or TypeError. Catch this in the main loop and flag the alert_id as "parsing_error".
Custom Exception: Define a TicketConflictError. As you process valid alerts, keep track of which incident ticket each host has been assigned to in this batch. A single ticket can cover multiple hosts, but a single host cannot be linked to two different tickets in the same batch. If a host is scheduled under a second, different ticket, raise this exception, deny the escalation, and flag the alert_id as "ticket_conflict".

4. Data Structures
Maintain a dictionary tracking the final assigned incident ticket for each host (e.g., {"192.168.1.15": "INC-4001"}).

Return a final summary dictionary containing:

"escalated_alerts": An integer count of fully processed and escalated alerts.
"host_tickets": The dictionary of hosts and their assigned incident tickets.
"failed_alerts": A nested dictionary grouping failed alert_ids by their error reason ("invalid_schema", "parsing_error", "ticket_conflict").

Sample Test Data

json
{
  "monitored_hosts": ["192.168.1.15", "192.168.1.16", "192.168.1.17", "192.168.1.18", "10.0.2.50"],
  "alert_batch": [
    {"alert_id": "A01", "host_ip": "192.168.1.15", "ticket_id": "INC-4001", "cvss_score": "7.5", "severity": "high"},
    {"alert_id": "A02", "host_ip": "192.168.9.99", "ticket_id": "INC-4002", "cvss_score": "9.1", "severity": "critical"},
    {"alert_id": "A03", "host_ip": "192.168.1.16", "ticket_id": "INC-4003", "cvss_score": "9.8", "severity": "critical"},
    {"alert_id": "A04", "host_ip": "192.168.1.17", "cvss_score": "6.2", "severity": "medium"},
    {"alert_id": "A05", "host_ip": "192.168.1.18", "ticket_id": "INC-4004", "cvss_score": "N/A", "severity": "high"},
    {"alert_id": "A06", "host_ip": "192.168.1.16", "ticket_id": "INC-4005", "cvss_score": "8.4", "severity": "critical"}
  ]
}