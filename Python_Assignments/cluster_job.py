import re


class NodeConflictError(Exception):
    """Raised when a task is scheduled for two different nodes within the same batch."""
    pass


def parse_memory(mem_string):
    """
    Convert a memory string like '512MB' or '2GB' into an integer
    representing Megabytes (MB). Assumes 1 GB = 1024MB.

    Raises:
        TypeError: if mem_string is not a string (e.g. None).
        ValueError: if mem_string doesn't match the expected pattern (e.g. 'Auto').
    """
    if not isinstance(mem_string, str):
        raise TypeError(f"Memory must be a string, got {type(mem_string).__name__}")

    cleaned = mem_string.strip()
    match = re.match(r'^(\d+(?:\.\d+)?)\s*(MB|GB)$', cleaned, re.IGNORECASE)
    if not match:
        raise ValueError(f"Cannot parse memory string: {mem_string!r}")

    value_str, unit = match.groups()
    value = float(value_str)
    if unit.lower() == 'gb':
        value *= 1024

    return int(value)


def process_job_schedule(job_batch, active_nodes):
    """
    Process a batch of job scheduling requests against a set of active cluster nodes.

    Returns a summary dict with:
        - successful_schedules: count of fully applied jobs
        - task_nodes: {task_id: assigned_node_id}
        - failed_jobs: {"invalid_schema": [...], "parsing_error": [...], "node_conflict": [...]}
    """
    URGENCY_ORDER = {"urgent": 0, "normal": 1, "low": 2}

    # Sort: urgent -> normal -> low. Unknown urgencies sink to the end,
    # and Python's sort is stable so original relative order is preserved within a group.
    sorted_batch = sorted(
        job_batch,
        key=lambda j: URGENCY_ORDER.get(j.get("urgency"), len(URGENCY_ORDER))
    )

    task_nodes = {}
    failed_jobs = {
        "invalid_schema": [],
        "parsing_error": [],
        "node_conflict": [],
    }
    successful_schedules = 0

    for job in sorted_batch:
        job_id = job.get("job_id", "UNKNOWN")
        node_id = job.get("node_id")

        # Skip jobs targeting nodes that aren't currently active
        if node_id not in active_nodes:
            continue

        # --- Schema validation ---
        try:
            task_id = job["task_id"]
            memory_raw = job["memory"]
        except KeyError:
            failed_jobs["invalid_schema"].append(job_id)
            continue

        # --- Memory parsing ---
        try:
            memory_mb = parse_memory(memory_raw)
        except (ValueError, TypeError):
            failed_jobs["parsing_error"].append(job_id)
            continue

        # --- Node conflict check & assignment ---
        try:
            existing_node = task_nodes.get(task_id)
            if existing_node is not None and existing_node != node_id:
                raise NodeConflictError(
                    f"Task {task_id} already assigned to node {existing_node}, "
                    f"cannot reassign to node {node_id} in the same batch"
                )
            task_nodes[task_id] = node_id
            successful_schedules += 1
        except NodeConflictError:
            failed_jobs["node_conflict"].append(job_id)
            continue

    return {
        "successful_schedules": successful_schedules,
        "task_nodes": task_nodes,
        "failed_jobs": failed_jobs,
    }


if __name__ == "__main__":
    import json

    active_nodes = {"N01", "N02", "N03", "N04", "N10"}
    job_batch = [
        {"job_id": "J01", "task_id": "T-501", "node_id": "N03", "memory": "512MB", "urgency": "normal"},
        {"job_id": "J02", "task_id": "T-777", "node_id": "N99", "memory": "256MB", "urgency": "urgent"},
        {"job_id": "J03", "task_id": "T-502", "node_id": "N01", "memory": "2GB", "urgency": "urgent"},
        {"job_id": "J04", "task_id": "T-503", "node_id": "N02", "urgency": "low"},
        {"job_id": "J05", "task_id": "T-504", "node_id": "N04", "memory": "Auto", "urgency": "normal"},
        {"job_id": "J06", "task_id": "T-502", "node_id": "N10", "memory": "128MB", "urgency": "urgent"},
    ]

    result = process_job_schedule(job_batch, active_nodes)
    print(json.dumps(result, indent=2))