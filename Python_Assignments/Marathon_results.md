# Task 26: Marathon Race Results System

## Problem Statement
A marathon organizer wants a program to record runners' finish times and generate ranked results.

## Requirements

Create the following functions:
- `add_runner(runners)`
- `record_finish_time(runners)`
- `get_ranked_results(runners)`
- `display_results(runners)`
- `get_podium(runners)`

The program should:

- Ask for the number of runners.
- Store each runner as a dictionary with a name, bib number, and finish time in minutes (starts as `None`, meaning "hasn't finished yet"), e.g. `{"name": "Kito", "bib": 101, "finish_time": None}`.
- Bib numbers should auto-increment starting from 101.
- Display a menu:
  ```
  1. View All Runners
  2. Record a Finish Time
  3. View Ranked Results
  4. View Podium (Top 3)
  5. Exit
  ```

If a finish time is recorded:
- Ask for the bib number.
- Check the runner exists.
- Ask for their finish time in minutes.
- Validate it's a positive number.
- Store it on that runner.

`get_ranked_results(runners)` should:
- Only consider runners who have actually finished (`finish_time` is not `None`).
- **Sort them by finish time, fastest first**, and return the sorted list. (Hint: look into Python's `sorted()` function and its `key` parameter.)

`display_results(runners)` should call `get_ranked_results` and print every finished runner in ranked order, showing their rank (1st, 2nd, 3rd...), name, bib number, and finish time.

`get_podium(runners)` should call `get_ranked_results` and return only the **top 3** finishers (or fewer, if fewer than 3 have finished).

Before exiting, display:
- Total number of runners registered
- Number of runners who have finished
- Number of runners who haven't finished yet
- The winner (fastest finish time), if any

## Concepts Tested
- Sorting (`sorted()` with a `key` function)
- Lists slicing (for top 3)
- Dictionaries
- Functions
- Loops
- Conditional statements
- Variables
- User input