from typing import Dict, List, Set, Tuple, Any

class NegativeCountError(Exception):
    """Custom exception raised when a sensor reports a vehicle count below zero."""
    pass

def validate_and_extract(log: Dict[str, Any]) -> Tuple[str, int]:
    """
    Validates a single log dictionary.
    Raises KeyError, ValueError, TypeError, or NegativeCountError on malformed data.
    """
    # Strict dictionary access to intentionally trigger a KeyError if keys are missing
    zone = log["zone"]
    raw_count = log["vehicle_count"]
    
    # Intentionally cast to trigger a ValueError or TypeError if the data is corrupt
    count = int(raw_count)
    
    if count < 0:
        raise NegativeCountError(f"Invalid count: {count}. Sensors cannot report negative vehicles.")
        
    return zone, count

def process_sensor_batch(batch_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Processes a batch of sensor logs, aggregating valid data and capturing failures.
    """
    zone_data: Dict[str, List[int]] = {}
    failed_sensors: Set[str] = set()
    calibrating_sensors: Set[str] = set()
    total_processed: int = 0
    
    for log in batch_data:
        # Default to UNKNOWN so we don't crash if the sensor_id itself is missing
        sensor_id = log.get("sensor_id", "UNKNOWN")
        status = log.get("status", "unknown")
        
        # Control Flow: Skip inactive sensors
        if status in ("offline", "maintenance"):
            continue
            
        # Exception Handling
        try:
            zone, count = validate_and_extract(log)
            
            # Data Structures: Nested aggregation
            if zone not in zone_data:
                zone_data[zone] = []
            zone_data[zone].append(count)
            
            total_processed += 1
            
        except KeyError:
            # Missing "zone" or "vehicle_count"
            failed_sensors.add(sensor_id)
        except (ValueError, TypeError):
            # "vehicle_count" was a string or incompatible type
            failed_sensors.add(sensor_id)
        except NegativeCountError:
            # Domain-specific business logic error
            calibrating_sensors.add(sensor_id)
            
    # Calculate zone averages using dictionary comprehension
    zone_averages = {
        zone: round(sum(counts) / len(counts), 2)
        for zone, counts in zone_data.items() if counts
    }
    
    return {
        "zone_averages": zone_averages,
        "failed_sensors": failed_sensors,
        "calibrating_sensors": calibrating_sensors,
        "total_processed": total_processed
    }

# --- Execution Block for Testing ---
if __name__ == "__main__":
    sample_data = [
      {"sensor_id": "S01", "zone": "CBD", "vehicle_count": 120, "status": "active"},
      {"sensor_id": "S02", "zone": "CBD", "vehicle_count": "N/A", "status": "active"},
      {"sensor_id": "S03", "zone": "Westlands", "vehicle_count": 45, "status": "active"},
      {"sensor_id": "S04", "zone": "Eastleigh", "status": "active"}, 
      {"sensor_id": "S05", "zone": "CBD", "vehicle_count": -15, "status": "active"},
      {"sensor_id": "S06", "zone": "Westlands", "vehicle_count": 80, "status": "maintenance"},
      {"sensor_id": "S07", "zone": "Eastleigh", "vehicle_count": 310, "status": "active"}
    ]

    result = process_sensor_batch(sample_data)
    
    import json
    print(json.dumps(result, indent=2))