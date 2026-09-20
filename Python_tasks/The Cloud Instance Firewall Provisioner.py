class SecurityGroupConflictError(Exception):
    """Raised when an instance is assigned to a second security group in the same batch."""
    pass


def parse_port(port_string):
    """
    Validate and coerce a port range string like "443/tcp" into an integer port number.
    Raises ValueError/TypeError on bad input, which the caller must handle.
    """
    if port_string is None:
        raise TypeError("Port string cannot be None")

    if not isinstance(port_string, str):
        raise TypeError("Port string must be a string")

    # Expect format "<port>/<protocol>"
    parts = port_string.split("/")
    if len(parts) != 2:
        raise ValueError(f"Malformed port string: {port_string!r}")

    port_part, protocol = parts

    # Raises ValueError for non-numeric strings like "Any"
    port = int(port_part)

    if not (1 <= port <= 65535):
        raise ValueError(f"Port {port} out of valid range (1-65535)")

    if protocol.lower() not in ("tcp", "udp"):
        raise ValueError(f"Unknown protocol: {protocol!r}")

    return port


def process_firewall_configs(task_batch, active_instances):
    TIER_ORDER = {"production": 0, "staging": 1, "development": 2}

    # Sort by tier priority; unknown tiers sink to the end
    sorted_batch = sorted(
        task_batch,
        key=lambda t: TIER_ORDER.get(t.get("tier"), len(TIER_ORDER))
    )

    successful_updates = 0
    instance_groups = {}  # instance_id -> assigned security_group
    failed_tasks = {
        "invalid_schema": [],
        "parsing_error": [],
        "sg_conflict": []
    }

    for task in sorted_batch:
        task_id = task.get("task_id", "UNKNOWN")

        # Skip tasks targeting instances that aren't active — silently ignored
        instance_id = task.get("instance_id")
        if instance_id not in active_instances:
            continue

        try:
            # Direct indexing (not .get()) so missing keys raise KeyError
            security_group = task["security_group"]
            raw_port_range = task["port_range"]

            # Delegate parsing/validation to the helper
            parse_port(raw_port_range)  # validated but not needed further here

            # Conflict check: same instance, different security group
            if instance_id in instance_groups:
                if instance_groups[instance_id] != security_group:
                    raise SecurityGroupConflictError(
                        f"Instance {instance_id} already assigned to "
                        f"{instance_groups[instance_id]}, cannot reassign to {security_group}"
                    )
                # Same group again — treat as a harmless repeat, still counts as success
            else:
                instance_groups[instance_id] = security_group

            successful_updates += 1

        except KeyError:
            failed_tasks["invalid_schema"].append(task_id)

        except (ValueError, TypeError):
            failed_tasks["parsing_error"].append(task_id)

        except SecurityGroupConflictError:
            failed_tasks["sg_conflict"].append(task_id)

    return {
        "successful_updates": successful_updates,
        "instance_groups": instance_groups,
        "failed_tasks": failed_tasks,
    }


# --- Sample run ---
if __name__ == "__main__":
    active_instances = {"i-001", "i-002", "i-003", "i-004", "i-005"}

    task_batch = [
        {"task_id": "F01", "instance_id": "i-001", "security_group": "sg-web", "port_range": "443/tcp", "tier": "staging"},
        {"task_id": "F02", "instance_id": "i-999", "security_group": "sg-db", "port_range": "5432/tcp", "tier": "production"},
        {"task_id": "F03", "instance_id": "i-002", "security_group": "sg-db", "port_range": "5432/tcp", "tier": "production"},
        {"task_id": "F04", "instance_id": "i-003", "security_group": "sg-web", "tier": "development"},
        {"task_id": "F05", "instance_id": "i-004", "security_group": "sg-cache", "port_range": "Any", "tier": "staging"},
        {"task_id": "F06", "instance_id": "i-002", "security_group": "sg-app", "port_range": "8080/tcp", "tier": "production"},
    ]

    result = process_firewall_configs(task_batch, active_instances)
    import json
    print(json.dumps(result, indent=2))