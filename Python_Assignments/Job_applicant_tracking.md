# Task 27: Job Applicant Tracking System

## Problem Statement
A company's HR department wants a program to track job applicants, their interview scores, and hiring eligibility.

## Requirements

Create the following functions:
- `add_applicant(applicants)`
- `record_interview_score(applicants)`
- `get_qualified_applicants(applicants, passing_score)`
- `all_stages_complete(applicant)`
- `display_ranked_applicants(applicants)`

The program should:

- Ask for the number of applicants.
- Store each applicant as a dictionary with a name, and a dictionary of interview stage scores, e.g. `{"name": "Tariq", "scores": {"phone_screen": None, "technical": None, "final": None}}`.
- All three stages (`phone_screen`, `technical`, `final`) start as `None` (not yet interviewed).
- Display a menu:
  ```
  1. View All Applicants
  2. Record an Interview Score
  3. View Qualified Applicants
  4. View Ranked Applicants (by average score)
  5. Exit
  ```

If a score is recorded:
- Ask for the applicant's name.
- Check the applicant exists.
- Show the three stage names and ask which one to record a score for.
- Validate it's one of the three valid stages.
- Ask for the score (0-100).
- Store it under that stage.

`all_stages_complete(applicant)` should return `True` if **none** of that applicant's three scores are still `None` (i.e., they've completed every stage), and `False` otherwise. (Hint: look into Python's `all()` function.)

`get_qualified_applicants(applicants, passing_score)` should return a list of applicants who:
- Have completed all interview stages (using `all_stages_complete`), **and**
- Have an average score across all three stages that meets or exceeds `passing_score`.

`display_ranked_applicants(applicants)` should show only applicants who have completed all stages, **ranked by their average score, highest first**.

Before exiting, display:
- Total number of applicants
- Number who have completed all interview stages
- Number who qualify with a passing average of 70 (using `get_qualified_applicants`)
- The top-ranked applicant (if any)

## Concepts Tested
- Nested dictionaries
- The `all()` built-in function
- Sorting (`sorted()` with a `key` function)
- Functions
- Loops
- Conditional statements
- Variables
- User input