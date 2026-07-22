# Custom Exception
class NegativeCountError(Exception):
    pass


# Helper Function
def validate_and_extract(log):
    sensor_id = log["sensor_id"]
    zone = log["zone"]
    vehicle_count = int(log["vehicle_count"])

    if vehicle_count < 0:
        raise NegativeCountError("Negative vehicle count")

    return sensor_id, zone, vehicle_count


# Main Function
def process_sensor_batch(batch_data):

    zone_data = {}
    failed_sensors = set()
    total_processed = 0

    for log in batch_data:

        # Ignore offline and maintenance sensors
        if log.get("status") in ["offline", "maintenance"]:
            continue

        try:
            sensor_id, zone, vehicle_count = validate_and_extract(log)

            if zone not in zone_data:
                zone_data[zone] = []

            zone_data[zone].append(vehicle_count)

            total_processed += 1

        except KeyError:
            failed_sensors.add(log.get("sensor_id", "Unknown"))

        except (ValueError, TypeError):
            failed_sensors.add(log.get("sensor_id", "Unknown"))

        except NegativeCountError:
            print(f"Sensor {log.get('sensor_id')} is calibrating.")
            failed_sensors.add(log.get("sensor_id"))