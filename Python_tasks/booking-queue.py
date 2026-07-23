#Booking queue 

class DoubleBookingError(Exception):
    pass
    
#Helper Function
def parse_duration(duration_value):
    try:
        duration = int(duration_value)
        return duration
    
    except(ValueError, TypeError):
        raise
    
    
#Main Function
def process_lab_bookings(booking_batch, lab_capacities):
    
    approved_bookings = []
    denied_capacity = []
    
    failed_requests = {
        "data_error": [],
        "policy_violation": []
    }    
    
    booked_students = set()
    
    #priority order
    priority_order = {
        "high": 1,
        "normal": 2,
        "low": 3
    }
    
    #sort bookings priority
    booking_batch.sort(key=lambda booking:priority_order[booking["priority"]])
    
    #process each booking
    for booking in booking_batch:
        
        try:
            req_id = booking["req_id"]
            student_id = booking["student_id"]
            lab = booking["lab"]
            duration = parse_duration(booking["duration"])
            
            #check for double booking
            if student_id in booked_students:
                raise DoubleBookingError
            
            #check lab capacity
            
            if duration > lab_capacities[lab]:
                denied_capacity.append(req_id)
                
            else:
                lab_capacities[lab] -= duration
                approved_bookings.append(req_id)
                booked_students.add(student_id)
                
                
        except KeyError:
            failed_requests["data_error"].append(
                booking.get("req_id", "Unknown")
            )          
        
        except(ValueError, TypeError):
            failed_requests["data_error"].append(
                booking.get("req_id", "Unknown")
            )
            
        except DoubleBookingError:
            failed_requests["policy_violation"].append(
                booking.get("req_id", "Unknown")
            )        
            
    summary = {
        "approved_bookings": approved_bookings,
        "denied_capacity": denied_capacity,
        "failed_requests": failed_requests,
        "remaining_capacities": lab_capacities
    }        
    
    return summary

#sample Data
lab_capacities = {
    "Network_Lab": 300,
    "Software_Lab": 200
}
                       

booking_batch = [
    {"req_id": "B01", "student_id": "EDU_01", "lab": "Network_Lab", "duration": 120, "priority": "normal"},
    {"req_id": "B02", "student_id": "EDU_02", "lab": "Software_Lab", "duration": "invalid_string", "priority": "high"},
    {"req_id": "B03", "student_id": "EDU_03", "duration": 60, "priority": "normal"},
    {"req_id": "B04", "student_id": "EDU_01", "lab": "Software_Lab", "duration": 90, "priority": "low"},
    {"req_id": "B05", "student_id": "EDU_05", "lab": "Network_Lab", "duration": 200, "priority": "high"},
    {"req_id": "B06", "student_id": "EDU_06", "lab": "Network_Lab", "duration": 60, "priority": "normal"}
]   

#Run the Program

result = process_lab_bookings(booking_batch, lab_capacities)

print("Final summary")
print(result)                         