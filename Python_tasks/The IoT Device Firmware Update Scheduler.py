class DeviceFlashConflictError(Exception):
    """Raised when a device is scheduled for a second, different firmware version in the same batch."""
    pass


def parse_version(version_string):
    """
    Validate and coerce a firmware version string like "v2.4.1" into a
    comparable tuple of integers, e.g. (2, 4, 1).
    Raises ValueError/TypeError on bad input, which the caller must handle.
    """
    if version_string is None:
        raise TypeError("Version string cannot be None")

    if not isinstance(version_string, str):
        raise TypeError("Version string must be a string")

    if not version_string.startswith("v"):
        raise ValueError(f"Malformed version string: {version_string!r}")

    body = version_string[1:]  # strip leading "v"
    parts = body.split(".")

    if not (1 <= len(parts) <= 3):
        raise ValueError(f"Malformed version string: {version_string!r}")

    # Raises ValueError for non-numeric segments like "latest"
    numeric_parts = [int(p) for p in parts]

    # Pad to always return a 3-tuple (major, minor, patch)
    while len(numeric_parts) < 3:
        numeric_parts.append(0)

    return tuple(numeric_parts)


def process_firmware_updates(job_batch, online_devices):
    PRIORITY_ORDER = {"critical": 0, "routine": 1, "optional": 2}

    # Sort by priority; unknown priorities sink to the end
    sorted_batch = sorted(
        job_batch,
        key=lambda j: PRIORITY_ORDER.get(j.get("priority"), len(PRIORITY_ORDER))
    )

    successful_updates = 0
    device_firmware = {}  # device_id -> applied firmware_version (string)
    failed_jobs = {
        "invalid_schema": [],
        "parsing_error": [],
        "flash_conflict": []
    }

    for job in sorted_batch:
        job_id = job.get("job_id", "UNKNOWN")

        # Skip jobs targeting devices that aren't online — silently ignored
        device_id = job.get("device_id")
        if device_id not in online_devices:
            continue

        try:
            # Direct indexing (not .get()) so missing keys raise KeyError
            zone = job["zone"]
            raw_version = job["firmware_version"]

            # Delegate parsing/validation to the helper
            parse_version(raw_version)  # validated but not needed further here

            # Conflict check: same device, different firmware version
            if device_id in device_firmware:
                if device_firmware[device_id] != raw_version:
                    raise DeviceFlashConflictError(
                        f"Device {device_id} already flashed with "
                        f"{device_firmware[device_id]}, cannot reflash with {raw_version}"
                    )
                # Same version again — harmless repeat, still counts as success
            else:
                device_firmware[device_id] = raw_version

            successful_updates += 1

        except KeyError:
            failed_jobs["invalid_schema"].append(job_id)

        except (ValueError, TypeError):
            failed_jobs["parsing_error"].append(job_id)

        except DeviceFlashConflictError:
            failed_jobs["flash_conflict"].append(job_id)

    return {
        "successful_updates": successful_updates,
        "device_firmware": device_firmware,
        "failed_jobs": failed_jobs,
    }


# --- Sample run ---
if __name__ == "__main__":
    online_devices = {"DEV_1001", "DEV_1002", "DEV_1003", "DEV_1004", "DEV_1005"}

    job_batch = [
        {"job_id": "J01", "device_id": "DEV_1001", "zone": "floor3", "firmware_version": "v2.4.1", "priority": "routine"},
        {"job_id": "J02", "device_id": "DEV_9999", "zone": "floor1", "firmware_version": "v1.0.0", "priority": "critical"},
        {"job_id": "J03", "device_id": "DEV_1002", "zone": "floor1", "firmware_version": "v3.2.0", "priority": "critical"},
        {"job_id": "J04", "device_id": "DEV_1003", "firmware_version": "v1.5.0", "priority": "optional"},
        {"job_id": "J05", "device_id": "DEV_1004", "zone": "floor2", "firmware_version": "latest", "priority": "routine"},
        {"job_id": "J06", "device_id": "DEV_1002", "zone": "floor1", "firmware_version": "v3.3.0", "priority": "critical"},
    ]

    result = process_firmware_updates(job_batch, online_devices)
    import json
    print(json.dumps(result, indent=2))