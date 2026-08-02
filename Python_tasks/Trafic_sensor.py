"""
Traffic Sensor Aggregation Pipeline
-----------------------------------
Processes a batch of unreliable sensor logs, skipping offline/maintenance
sensors, validating each remaining log, aggregating vehicle counts by zone,
and returning a summary with zone averages, failed sensors, and a count of
successfully processed logs.
"""


class NegativeCountError(Exception):
    """Raised when a sensor reports a vehicle_count below zero."""


def validate_and_extract(log):
    """
    Validate a single sensor log and extract (zone, vehicle_count).

    Raises:
        KeyError: if 'zone' or 'vehicle_count' is missing.
        (TypeError, ValueError): if vehicle_count can't be converted to int.
        NegativeCountError: if vehicle_count is negative.
    """
    # This will raise KeyError naturally if either key is absent.
    zone = log["zone"]
    raw_count = log["vehicle_count"]

    # This will raise ValueError (e.g. "N/A") or TypeError (e.g. None) if
    # raw_count isn't something that can become an int.
    vehicle_count = int(raw_count)

    if vehicle_count < 0:
        raise NegativeCountError(
            f"Sensor {log.get('sensor_id', 'UNKNOWN')} reported a negative count: {vehicle_count}"
        )

    return zone, vehicle_count


def process_sensor_batch(batch_data):
    """
    Process a batch of raw sensor logs into a summary report.

    Returns:
        {
            "zone_averages": {zone: avg_vehicle_count, ...},
            "failed_sensors": {sensor_id, ...},
            "total_processed": int
        }
    """
    zone_counts = {}          # {zone: [count1, count2, ...]}
    failed_sensors = set()    # unique sensor_ids that threw an exception
    total_processed = 0
    total_failed = 0

    for log in batch_data:
        status = log.get("status")
        if status in ("offline", "maintenance"):
            continue  # ignore these entirely, not a pass/fail case

        sensor_id = log.get("sensor_id", "UNKNOWN")

        try:
            zone, vehicle_count = validate_and_extract(log)
            zone_counts.setdefault(zone, []).append(vehicle_count)
            total_processed += 1

        except KeyError:
            # Missing 'zone' or 'vehicle_count' field
            failed_sensors.add(sensor_id)
            total_failed += 1

        except (TypeError, ValueError):
            # vehicle_count wasn't a usable number (e.g. "N/A", "ERR_TIMEOUT")
            failed_sensors.add(sensor_id)
            total_failed += 1

        except NegativeCountError:
            # Sensor is reporting a physically impossible count
            failed_sensors.add(sensor_id)
            total_failed += 1

    zone_averages = {
        zone: round(sum(counts) / len(counts), 2)
        for zone, counts in zone_counts.items()
    }

    return {
        "zone_averages": zone_averages,
        "failed_sensors": failed_sensors,
        "total_processed": total_processed,
        "total_failed": total_failed,  # bonus, not required but useful
    }


if __name__ == "__main__":
    sample_data = [
        {"sensor_id": "S01", "zone": "CBD", "vehicle_count": 120, "status": "active"},
        {"sensor_id": "S02", "zone": "CBD", "vehicle_count": "N/A", "status": "active"},
        {"sensor_id": "S03", "zone": "Westlands", "vehicle_count": 45, "status": "active"},
        {"sensor_id": "S04", "zone": "Eastleigh", "status": "active"},
        {"sensor_id": "S05", "zone": "CBD", "vehicle_count": -15, "status": "active"},
        {"sensor_id": "S06", "zone": "Westlands", "vehicle_count": 80, "status": "maintenance"},
        {"sensor_id": "S07", "zone": "Eastleigh", "vehicle_count": 310, "status": "active"},
    ]

    result = process_sensor_batch(sample_data)

    print("--- Summary ---")
    print("Zone Averages:", result["zone_averages"])
    print("Failed Sensors:", result["failed_sensors"])
    print("Total Processed:", result["total_processed"])
    print("Total Failed:", result["total_failed"])