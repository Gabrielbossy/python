# Task 4: Student Grade Management System

## Problem Statement
A school wants a program to manage student grades and calculate their performance.

## Requirements

Create the following functions:
- `add_student(students)`
- `add_grade(students)`
- `calculate_average(grades)`
- `display_students(students)`

The program should:

- Ask for the number of students.
- Store each student as a dictionary with a name and an empty list of grades, e.g. `{"name": "John", "grades": []}`.
- Display a menu:
  ```
  1. Add Grade to Student
  2. View All Students and Averages
  3. View Top Student
  4. Exit
  ```

If a user adds a grade:
- Ask which student (by name).
- Ask for the grade (0–100).
- Validate the grade is within range.
- Append it to that student's grade list.

When viewing students, show each student's name, their grades, and their average (using `calculate_average`).

When viewing the top student, find whichever student has the highest average grade.

Before exiting, display:
- Total number of students
- Total number of grades entered across all students
- The class-wide average (average of all grades combined)

## Concepts Tested
- Dictionaries
- Lists
- Functions
- Loops
- Conditional statements
- Variables
- User input
- List/dictionary manipulation


