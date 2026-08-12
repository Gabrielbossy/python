# Task 10: Parking Lot Management System

## Problem Statement
A parking garage wants a program to manage vehicle check-ins and check-outs, and calculate parking fees.

## Requirements

Create the following functions:
- `display_spots(spots)`
- `check_in(spots, parked_vehicles)`
- `check_out(spots, parked_vehicles)`
- `calculate_fee(hours_parked, hourly_rate)`

The program should:

- Ask for the number of parking spots.
- Create a list of spot numbers, e.g. `[1, 2, 3, 4, 5]`.
- Display a menu:
  ```
  1. View Available Spots
  2. Check In Vehicle
  3. Check Out Vehicle
  4. View Parked Vehicles
  5. Exit
  ```

If a vehicle checks in:
- Show available spots.
- Ask for the vehicle's license plate number.
- Ask which spot to park in.
- Check the spot is actually available.
- Remove the spot from available spots.
- Store the vehicle as a dictionary with plate number, spot number, and hours parked (start at 0), e.g. `{"plate": "KDA123X", "spot": 3, "hours": 0}`, and add it to `parked_vehicles`.

If a vehicle checks out:
- Ask for the license plate number.
- Check if that vehicle is currently parked.
- Ask how many hours it was parked.
- Calculate the fee (using `calculate_fee`, with a fixed hourly rate, e.g. $2/hour).
- Remove the vehicle from `parked_vehicles` and return its spot to the available spots list.
- Display the fee charged.

When viewing parked vehicles, show every vehicle's plate number and spot number.

Before exiting, display:
- Total number of spots
- Number of spots currently available
- Number of vehicles currently parked
- Total revenue collected from all checkouts

## Concepts Tested
- Dictionaries
- Lists
- Functions
- Loops
- Conditional statements
- Variables
- User input
- List/dictionary manipulation
