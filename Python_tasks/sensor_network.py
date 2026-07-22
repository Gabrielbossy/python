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
            
    #calculate zone average
            
    zone_averages = {}
    
    for zone in zone_data:
        average = sum(zone_data[zone])/len(zone_data[zone])
        zone_averages[zone] = round(average, 2)
        
    summary = {
        "zone_averages": zone_averages,
        "failed_sensors": failed_sensors,
        "total_processed": total_processed
        
    }     
    
    return summary

#sample Test Data
batch_data = [
    {"sensor_id": "S01", "zone": "CBD", "vehicle_count": 120, "status": "active"},
    {"sensor_id": "S02", "zone": "CBD", "vehicle_count": "N/A", "status": "active"},
    {"sensor_id": "S03", "zone": "Westlands", "vehicle_count": 45, "status": "active"},
    {"sensor_id": "S04", "zone": "Eastleigh", "status": "active"},
    {"sensor_id": "S05", "zone": "CBD", "vehicle_count": -15, "status": "active"},
    {"sensor_id": "S06", "zone": "Westlands", "vehicle_count": 80, "status": "maintenance"},
    {"sensor_id": "S07", "zone": "Eastleigh", "vehicle_count": 310, "status": "active"}
]


#Result
result = process_sensor_batch(batch_data)

print("\nFinal Summary")
print(result)
