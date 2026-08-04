# Task 6: Employee Payroll System

## Problem Statement
A small company wants a program to manage employee work hours and calculate their pay.

## Requirements

Create the following functions:
- `add_employee(employees)`
- `log_hours(employees)`
- `calculate_pay(hours_worked, hourly_rate)`
- `display_employees(employees)`

The program should:

- Ask for the number of employees.
- Store each employee as a dictionary with a name, hourly rate, and hours worked, e.g. `{"name": "Jane", "hourly_rate": 15, "hours_worked": 0}`.
- Display a menu:
  ```
  1. Log Hours for Employee
  2. View All Employees & Pay
  3. View Highest Paid Employee
  4. Exit
  ```

If a user logs hours:
- Ask which employee (by name).
- Ask how many hours they worked.
- Validate the hours are positive.
- Add the hours to that employee's total hours worked.

When viewing employees, show each employee's name, hourly rate, total hours worked, and total pay (using `calculate_pay`).

When viewing the highest paid employee, find whichever employee has the highest total pay.

Before exiting, display:
- Total number of employees
- Total hours logged across all employees
- Total payroll amount (sum of everyone's pay)

## Concepts Tested
- Dictionaries
- Lists
- Functions
- Loops
- Conditional statements
- Variables
- User input
- List/dictionary manipulation
