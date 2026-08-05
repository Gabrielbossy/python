# Assignment: University Computer Lab Access System

## Background

A university wants to automate access to its computer laboratories. Students submit access requests throughout the day. Your program must validate each request, assign students to labs, and prevent duplicate lab assignments.

---

## Input

Your program receives:

- A list of access request dictionaries.
- A set of active laboratory names.

A valid request looks like:

```python
{
    "request_id": "A01",
    "student_id": "ST100",
    "lab": "Networking",
    "duration": "2hours",
    "priority": "high"
}
```

---

## Requirements

### 1. Functions & Architecture

Create:

- `process_lab_requests(request_batch, active_labs)`
- `parse_duration(duration_string)`

The helper function should convert:

- `"2hours"` → `2`
- `"5hours"` → `5`

---

### 2. Control Flow

Sort requests by priority:

1. high
2. normal
3. low

Loop through every request.

If the requested lab is not in the active labs set, ignore the request and continue.

---

### 3. Exceptions

Handle these errors:

#### Missing Keys

Some requests may not contain `student_id` or `duration`.

Store their `request_id` under `"invalid_request"`.

#### Parsing Errors

If duration is `"all day"` or `None`, raise and catch a `ValueError` or `TypeError`.

Store the `request_id` under `"invalid_duration"`.

#### Custom Exception

Create a custom exception named `DuplicateLabError`.

A student cannot be assigned to two different labs in the same batch.

If that happens:

- Raise `DuplicateLabError`
- Store the `request_id` under `"duplicate_assignment"`

---

### 4. Data Structures

Maintain a dictionary showing the final assigned lab for every student.

Return a summary dictionary containing:

- successful_requests
- student_labs
- failed_requests

---

## Sample Data

```python
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
```