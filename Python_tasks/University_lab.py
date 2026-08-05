# Custom Exception
class DuplicateLabError(Exception):
    pass


# Helper Function
def parse_duration(duration_string):
    try:
        if duration_string.endswith("hours"):
            return int(duration_string.replace("hours", ""))
        else:
            raise ValueError("Invalid duration")

    except (ValueError, TypeError):
        raise


# Main Function
def process_lab_requests(request_batch, active_labs):

    successful_requests = 0

    student_labs = {}

    failed_requests = {
        "invalid_request": [],
        "invalid_duration": [],
        "duplicate_assignment": []
    }

    priority_order = {
        "high": 1,
        "normal": 2,
        "low": 3
    }

    request_batch.sort(key=lambda request: priority_order[request["priority"]])

    for request in request_batch:

        try:
            request_id = request["request_id"]
            student_id = request["student_id"]
            lab = request["lab"]
            duration = parse_duration(request["duration"])

            if lab not in active_labs:
                continue

            if student_id in student_labs and student_labs[student_id] != lab:
                raise DuplicateLabError

            student_labs[student_id] = lab
            successful_requests += 1

        except KeyError:
            failed_requests["invalid_request"].append(
                request.get("request_id", "Unknown")
            )

        except (ValueError, TypeError):
            failed_requests["invalid_duration"].append(
                request.get("request_id", "Unknown")
            )

        except DuplicateLabError:
            failed_requests["duplicate_assignment"].append(
                request.get("request_id", "Unknown")
            )

    summary = {
        "successful_requests": successful_requests,
        "student_labs": student_labs,
        "failed_requests": failed_requests
    }

    return summary


# Sample Data
active_labs = {
    "Networking",
    "Programming",
    "Cyber Security"
}

request_batch = [
    {"request_id":"A01","student_id":"ST100","lab":"Networking","duration":"2hours","priority":"normal"},
    {"request_id":"A02","student_id":"ST101","lab":"Programming","duration":"3hours","priority":"high"},
    {"request_id":"A03","student_id":"ST102","lab":"AI Lab","duration":"2hours","priority":"high"},
    {"request_id":"A04","student_id":"ST103","lab":"Cyber Security","priority":"low"},
    {"request_id":"A05","student_id":"ST104","lab":"Networking","duration":"all day","priority":"normal"},
    {"request_id":"A06","student_id":"ST101","lab":"Cyber Security","duration":"1hours","priority":"high"}
]

result = process_lab_requests(request_batch, active_labs)

print(result)