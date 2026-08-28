# Task 20: Vaccine Appointment Scheduling System

## Problem Statement
A health clinic wants a program to manage vaccine appointment slots for patients.

## Requirements

Create the following functions:
- `add_slot(slots)`
- `book_appointment(slots, appointments)`
- `cancel_appointment(slots, appointments)`
- `calculate_doses_given(appointments)`
- `display_slots(slots)`

The program should:

- Ask for the number of time slots to create.
- Store each slot as a dictionary with a slot ID, time, capacity, and number of patients booked, e.g. `{"slot_id": 1, "time": "9:00 AM", "capacity": 3, "booked": 0}`.
- Display a menu:
  ```
  1. View All Slots
  2. Book Appointment
  3. Cancel Appointment
  4. View Appointment Records
  5. Exit
  ```

If a patient books an appointment:
- Show available slots (where `booked` is less than `capacity`).
- Ask for the slot ID.
- Check the slot exists and still has space.
- Ask for the patient's name.
- Increase the slot's `booked` count by 1.
- Store the appointment as a dictionary with slot ID, patient name, and time, and add it to `appointments`.

If a patient cancels an appointment:
- Ask for the patient's name.
- Check if they have an appointment booked.
- Decrease the matching slot's `booked` count by 1.
- Remove the matching record from `appointments`.

When viewing appointment records, show every patient's name, slot ID, and time.

Before exiting, display:
- Total number of slots
- Total appointment capacity across all slots
- Number of doses given (using `calculate_doses_given` — this is simply the number of active appointments)
- The slot with the most bookings

## Concepts Tested
- Dictionaries
- Lists
- Functions
- Loops
- Conditional statements
- Variables
- User input
- List/dictionary manipulation