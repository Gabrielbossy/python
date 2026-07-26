# Custom Exception
class AgentOverloadError(Exception):
    pass


# Helper Function
def validate_demographics(age_value, symptoms_list):
    try:
        age = int(age_value)

        if not isinstance(symptoms_list, list):
            raise TypeError("Symptoms must be a list.")

        return age, symptoms_list

    except (ValueError, TypeError):
        raise


# Main Function
def dispatch_patients(query_batch, agent_loads):

    successful_routes = {}

    manual_nurse_review = set()

    fallback_queue = []

    failed_queries = {
        "incomplete_record": [],
        "data_error": []
    }

    # Urgency order
    urgency_order = {
        "critical": 1,
        "high": 2,
        "standard": 3
    }

    # Sort queries
    query_batch.sort(key=lambda query: urgency_order[query["urgency"]])

    # Process each patient
    for query in query_batch:

        try:
            patient_id = query["patient_id"]
            age, symptoms = validate_demographics(
                query["age"],
                query["symptoms"]
            )

            target_agent = query["target_agent"]

            # Agent does not exist
            if target_agent not in agent_loads:
                fallback_queue.append(patient_id)
                continue

            # Check agent capacity
            if agent_loads[target_agent] >= 5:
                raise AgentOverloadError

            # Increase load
            agent_loads[target_agent] += 1

            # Store successful routes
            if target_agent not in successful_routes:
                successful_routes[target_agent] = []

            successful_routes[target_agent].append(patient_id)

        except KeyError:
            failed_queries["incomplete_record"].append(
                query.get("patient_id", "Unknown")
            )

        except (ValueError, TypeError):
            failed_queries["data_error"].append(
                query.get("patient_id", "Unknown")
            )

        except AgentOverloadError:
            manual_nurse_review.add(
                query.get("patient_id", "Unknown")
            )

    summary = {
        "successful_routes": successful_routes,
        "manual_nurse_review": manual_nurse_review,
        "failed_queries": failed_queries,
        "final_agent_loads": agent_loads,
        "fallback_queue": fallback_queue
    }

    return summary


# Sample Data
agent_loads = {
    "Triage": 2,
    "Pediatrics": 4,
    "Pharmacy": 1
}

query_batch = [
    {"patient_id": "P01", "age": 45, "symptoms": "headache", "urgency": "standard", "target_agent": "Triage"},
    {"patient_id": "P02", "age": 8, "symptoms": ["fever", "rash"], "urgency": "critical", "target_agent": "Pediatrics"},
    {"patient_id": "P03", "age": "thirty", "symptoms": ["cough"], "urgency": "high", "target_agent": "Triage"},
    {"patient_id": "P04", "age": 65, "symptoms": ["chest pain"], "urgency": "critical", "target_agent": "Cardiology"},
    {"patient_id": "P05", "age": 3, "symptoms": ["crying"], "urgency": "high", "target_agent": "Pediatrics"},
    {"patient_id": "P06", "age": 12, "symptoms": ["sprained ankle"], "urgency": "standard", "target_agent": "Pediatrics"}
]

# Run the program
result = dispatch_patients(query_batch, agent_loads)

print("Final Summary")
print(result)