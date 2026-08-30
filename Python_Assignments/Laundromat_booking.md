# Task 22: Laundromat Machine Booking System

## Problem Statement
A laundromat wants a program to manage its washing machines and dryers, tracking usage and payments.

## Requirements

Create the following functions:
- `add_machine(machines)`
- `start_cycle(machines, sessions)`
- `end_cycle(machines, sessions)`
- `calculate_charge(minutes, rate_per_minute)`
- `display_machines(machines)`

The program should:

- Ask for the number of machines.
- Store each machine as a dictionary with a machine ID, type (`"Washer"` or `"Dryer"`), and status, e.g. `{"machine_id": 1, "type": "Washer", "status": "Free"}`.
- Rates:
  - Washer: $0.10/minute
  - Dryer: $0.08/minute
- Display a menu:
  ```
  1. View All Machines
  2. Start a Cycle
  3. End a Cycle
  4. View Active Sessions
  5. Exit
  ```

If a customer starts a cycle:
- Show free machines.
- Ask for the machine ID.
- Check the machine exists and is free.
- Ask for the customer's name.
- Mark the machine's status as "In Use".
- Store the session as a dictionary with machine ID, customer name, and machine type, and add it to `sessions`.

If a customer ends a cycle:
- Ask for the machine ID.
- Check the machine exists and is currently "In Use".
- Ask how many minutes the cycle ran.
- Calculate the charge (using `calculate_charge`, based on the machine's type rate).
- Mark the machine's status back to "Free".
- Remove the matching record from `sessions`.
- Display the charge.

When viewing active sessions, show every machine ID, customer name, and machine type currently in use.

Before exiting, display:
- Total number of machines
- Number of machines currently free
- Number of machines currently in use
- Total revenue collected from all completed cycles

## Concepts Tested
- Dictionaries
- Lists
- Functions
- Loops
- Conditional statements
- Variables
- User input
- List/dictionary manipulation