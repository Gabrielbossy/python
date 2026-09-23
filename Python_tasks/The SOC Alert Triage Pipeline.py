class TicketConflictError(Exception):
    """Raised when a host is linked to a second, different incident ticket in the same batch."""
    pass


def parse_cvss(cvss_string):
    """
    Validate and coerce a CVSS score string like "7.5" into a float
    within the valid CVSS range of 0.0-10.0.
    Raises ValueError/TypeError on bad input, which the caller must handle.
    """
    if cvss_string is None:
        raise TypeError("CVSS score cannot be None")

    # Raises ValueError for strings like "N/A",
    # TypeError for unsupported types (e.g. list, dict)
    score = float(cvss_string)

    if not (0.0 <= score <= 10.0):
        raise ValueError(f"CVSS score {score} out of valid range (0.0-10.0)")

    return score


def process_soc_alerts(alert_batch, monitored_hosts):
    SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2}

    # Sort by severity priority; unknown severities sink to the end
    sorted_batch = sorted(
        alert_batch,
        key=lambda a: SEVERITY_ORDER.get(a.get("severity"), len(SEVERITY_ORDER))
    )

    escalated_alerts = 0
    host_tickets = {}  # host_ip -> assigned ticket_id
    failed_alerts = {
        "invalid_schema": [],
        "parsing_error": [],
        "ticket_conflict": []
    }

    for alert in sorted_batch:
        alert_id = alert.get("alert_id", "UNKNOWN")

        # Skip alerts targeting hosts that aren't monitored — silently ignored
        host_ip = alert.get("host_ip")
        if host_ip not in monitored_hosts:
            continue

        try:
            # Direct indexing (not .get()) so missing keys raise KeyError
            ticket_id = alert["ticket_id"]
            raw_cvss = alert["cvss_score"]

            # Delegate parsing/validation to the helper
            parse_cvss(raw_cvss)  # validated but not needed further here

            # Conflict check: same host, different ticket
            if host_ip in host_tickets:
                if host_tickets[host_ip] != ticket_id:
                    raise TicketConflictError(
                        f"Host {host_ip} already linked to "
                        f"{host_tickets[host_ip]}, cannot reassign to {ticket_id}"
                    )
                # Same ticket again — harmless repeat, still counts as escalated
            else:
                host_tickets[host_ip] = ticket_id

            escalated_alerts += 1

        except KeyError:
            failed_alerts["invalid_schema"].append(alert_id)

        except (ValueError, TypeError):
            failed_alerts["parsing_error"].append(alert_id)

        except TicketConflictError:
            failed_alerts["ticket_conflict"].append(alert_id)

    return {
        "escalated_alerts": escalated_alerts,
        "host_tickets": host_tickets,
        "failed_alerts": failed_alerts,
    }


# --- Sample run ---
if __name__ == "__main__":
    monitored_hosts = {"192.168.1.15", "192.168.1.16", "192.168.1.17", "192.168.1.18", "10.0.2.50"}

    alert_batch = [
        {"alert_id": "A01", "host_ip": "192.168.1.15", "ticket_id": "INC-4001", "cvss_score": "7.5", "severity": "high"},
        {"alert_id": "A02", "host_ip": "192.168.9.99", "ticket_id": "INC-4002", "cvss_score": "9.1", "severity": "critical"},
        {"alert_id": "A03", "host_ip": "192.168.1.16", "ticket_id": "INC-4003", "cvss_score": "9.8", "severity": "critical"},
        {"alert_id": "A04", "host_ip": "192.168.1.17", "cvss_score": "6.2", "severity": "medium"},
        {"alert_id": "A05", "host_ip": "192.168.1.18", "ticket_id": "INC-4004", "cvss_score": "N/A", "severity": "high"},
        {"alert_id": "A06", "host_ip": "192.168.1.16", "ticket_id": "INC-4005", "cvss_score": "8.4", "severity": "critical"},
    ]

    result = process_soc_alerts(alert_batch, monitored_hosts)
    import json
    print(json.dumps(result, indent=2))