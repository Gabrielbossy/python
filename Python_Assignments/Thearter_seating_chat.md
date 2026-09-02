# Task 25: Theater Seating Chart System

## Problem Statement
A theater wants a program to manage a seating chart laid out as **rows and columns** (a grid), not just a flat list of seats.

## Requirements

Create the following functions:
- `create_seating_chart(rows, columns)`
- `book_seat(chart, row, column)`
- `display_chart(chart)`
- `count_available_seats(chart)`

The program should:

- Ask for the number of rows and number of columns.
- Represent the seating chart as a **list of lists** (a 2D grid), where each seat is either `"O"` (open/available) or `"X"` (booked). For example, a 2-row, 3-column chart would start as:
  ```
  [["O", "O", "O"],
   ["O", "O", "O"]]
  ```
- Display a menu:
  ```
  1. View Seating Chart
  2. Book a Seat
  3. View Available Seat Count
  4. Exit
  ```

`create_seating_chart(rows, columns)` should build and return the initial grid — use a **nested loop** (a loop inside a loop) to build it: the outer loop builds each row, the inner loop fills that row with `"O"` for each column.

If a customer books a seat:
- Ask for the row number and column number (use numbering starting at 1 for the customer, e.g. "Row 1, Seat 1" — but remember Python lists are indexed from 0 internally, so you'll need to convert).
- Validate the row and column are within range of the chart's size.
- Check the seat is currently `"O"` (open).
- Change that seat to `"X"` (booked).
- Display a confirmation message.

`display_chart(chart)` should print the grid so it looks like an actual seating layout — use a nested loop to print every seat in every row, with rows on separate lines.

`count_available_seats(chart)` should use a nested loop to go through every seat in the grid and return how many are still `"O"`.

Before exiting, display:
- Total number of seats in the chart (rows × columns)
- Number of seats still available (using `count_available_seats`)
- Number of seats booked

## Concepts Tested
- 2D Lists (lists of lists / grids)
- Nested loops
- Functions
- Conditional statements
- Variables
- User input
- List manipulation (indexing rows and columns)