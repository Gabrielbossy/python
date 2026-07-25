The Problem: The Medical AI Dispatcher
Background:
You are building the core routing engine for a clinic's multi-agent healthcare platform. Patient queries arrive in a continuous stream. Your script must evaluate the severity of each query, sanitize the data, and route the patient to the correct specialized AI agent (e.g., Triage, Pediatrics, Pharmacy) without overloading any single agent.

The Input:
You receive a list of patient request dictionaries and a dictionary mapping available agents to their current active load (number of patients currently being handled).
A valid request looks like this:
{"patient_id": "P01", "age": 8, "symptoms": ["fever", "rash"], "urgency": "high", "target_agent": "Pediatrics"}

The Requirements:

1. Functions & Architecture
Write a main function called dispatch_patients(query_batch, agent_loads).

Write a helper function called validate_demographics(age_value, symptoms_list) to isolate the validation of the patient's physical data.

2. Control Flow
Before processing, sort the queries by urgency. "critical" queries must be routed first, followed by "high", and finally "standard".

Iterate through the sorted batch.

If a request targets an agent that does not exist in the agent_loads dictionary, ignore the routing and add the patient_id to a fallback queue.

3. Exceptions
Anticipate and handle these failure modes using explicit try/except blocks:

Missing Keys: Some queries will be missing the target_agent or symptoms keys. Catch this KeyError and flag the patient_id as "incomplete_record".

Invalid Types: Sometimes age comes in as a string like "eight" or symptoms comes in as a single string instead of a List. Your helper function should check this and raise a ValueError or TypeError. Catch this in the main loop and flag the patient_id as "data_error".

Custom Exception: Define an AgentOverloadError. Each agent has a strict maximum capacity of 5 concurrent patients. As you route patients, increment that agent's load. If an agent reaches a load of 5, and another patient is routed to them, raise this exception, deny the routing, and place the patient_id in a "manual_nurse_review" set.

4. Data Structures
Maintain the updated agent_loads dictionary dynamically as you approve routes.

Return a final summary dictionary containing:

"successful_routes": A dictionary mapping agent names to a List of patient_ids newly assigned to them.

"manual_nurse_review": A Set of patient_ids that hit an overloaded agent.

"failed_queries": A nested dictionary grouping failed patient_ids by their error reason ("incomplete_record", "data_error").

"final_agent_loads": The updated agent_loads dictionary.

Sample Test Data
Here is the JSON payload to test the script:

JSON
{
  "agent_loads": {
    "Triage": 2,
    "Pediatrics": 4,
    "Pharmacy": 1
  },
  "query_batch": [
    {"patient_id": "P01", "age": 45, "symptoms": "headache", "urgency": "standard", "target_agent": "Triage"},
    {"patient_id": "P02", "age": 8, "symptoms": ["fever", "rash"], "urgency": "critical", "target_agent": "Pediatrics"},
    {"patient_id": "P03", "age": "thirty", "symptoms": ["cough"], "urgency": "high", "target_agent": "Triage"},
    {"patient_id": "P04", "age": 65, "symptoms": ["chest pain"], "urgency": "critical", "target_agent": "Cardiology"},
    {"patient_id": "P05", "age": 3, "symptoms": ["crying"], "urgency": "high", "target_agent": "Pediatrics"},
    {"patient_id": "P06", "age": 12, "symptoms": ["sprained ankle"], "urgency": "standard", "target_agent": "Pediatrics"}
  ]
}