class AgentOverLoadError(Exception):
    pass

# Helper Function
def validate_demographics(age_value, symptoms_list):
    try:
        age = int(age_value)
        
        if not isinstance(symptoms_list, list):
            raise TypeError("symptoms must be a list.")
        
        return age(symptoms_list)
    
    except(ValueError, TypeError)
    raise

# Main Function