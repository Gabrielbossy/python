# Task 18: Restaurant Table Reservation System

## Problem Statement
A restaurant wants a program to manage table reservations for its dining room.

## Requirements

Create the following functions:
- `add_table(tables)`
- `reserve_table(tables, reservations)`
- `cancel_reservation(tables, reservations)`
- `calculate_deposit(party_size, rate_per_person)`
- `display_tables(tables)`

The program should:

- Ask for the number of tables in the restaurant.
- Store each table as a dictionary with a table number, seating capacity, and status, e.g. `{"table_number": 1, "capacity": 4, "status": "Free"}`.
- Display a menu:
  ```
  1. View All Tables
  2. Reserve a Table
  3. Cancel a Reservation
  4. View Active Reservations
  5. Exit
  ```

If a customer reserves a table:
- Show free tables.
- Ask for the table number.
- Check the table exists and is free.
- Ask for the customer's name and party size.
- Check the party size does not exceed the table's capacity.
- Calculate a deposit (using `calculate_deposit`, at a fixed rate of $5 per person).
- Mark the table's status as "Reserved".
- Store the reservation as a dictionary with table number, customer name, party size, and deposit paid, and add it to `reservations`.
- Display the deposit charged.

If a reservation is cancelled:
- Ask for the table number.
- Check if that table currently has an active reservation.
- Mark the table's status back to "Free".
- Remove the matching record from `reservations`.

When viewing active reservations, show each reservation's table number, customer name, party size, and deposit paid.

Before exiting, display:
- Total number of tables
- Number of tables currently free
- Number of tables currently reserved
- Total deposits collected from all reservations

## Concepts Tested
- Dictionaries
- Lists
- Functions
- Loops
- Conditional statements
- Variables
- User input
- List/dictionary manipulation