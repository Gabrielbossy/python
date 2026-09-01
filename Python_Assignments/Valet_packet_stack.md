# Task 24: Valet Parking Stack System

## Problem Statement
A valet parking service has a **single-lane driveway** — cars are parked one behind another, so the only car that can be retrieved at any time is the **last one parked** (like a stack of plates: you can only take from the top). The valet company wants a program to manage this.

## Requirements

Create the following functions:
- `park_car(lane, parked_cars)`
- `retrieve_last_car(lane, parked_cars)`
- `view_lane(lane)`
- `total_cars_parked(parked_cars)`

The program should:

- Start with an empty lane (a list) and an empty list of `parked_cars` (a historical record of every car that has ever been parked, including ones already retrieved).
- Store each car as a dictionary with a license plate and owner name, e.g. `{"plate": "KDA123X", "owner": "Musa"}`.
- Display a menu:
  ```
  1. Park a Car
  2. Retrieve Last Parked Car
  3. View Lane
  4. View Parking History
  5. Exit
  ```

If a car is parked:
- Ask for the license plate and owner's name.
- Add the car to the **top** of the lane (the end of the list).
- Also record it in `parked_cars` (this list should never shrink, even when cars leave — it's a permanent history).

If a car is retrieved:
- Check the lane isn't empty.
- **Remove the car from the top of the lane** (the end of the list, not the front — this is the key rule of a stack).
- Display which car was retrieved.

**Important note for whoever solves this:** if the valet needs a car that is *not* at the top (buried behind others), in real life they'd have to move every car in front of it out of the way first, park them elsewhere temporarily, retrieve the buried car, then put everything back. This program does **not** need to implement that — just the simple "always retrieve the top/last one" behavior is enough for these requirements.

When viewing the lane, show every car currently parked, from the top of the stack (last parked, retrieved first) down to the bottom.

`total_cars_parked(parked_cars)` should calculate and return how many cars have ever been parked (the length of the historical record). Call it as part of the final summary.

Before exiting, display:
- Total cars ever parked (using `total_cars_parked`)
- Number of cars currently in the lane
- Number of cars retrieved so far
- The car currently at the top of the lane (if any)

## Concepts Tested
- Lists (used as a stack / LIFO structure)
- Dictionaries
- Functions
- Loops
- Conditional statements
- Variables
- User input
- List manipulation (`append`/`pop` from the end)