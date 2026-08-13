# Task 11: Gym Membership Management System

## Problem Statement
A gym wants a program to manage its members, their membership plans, and payments.

## Requirements

Create the following functions:
- `register_member(members)`
- `renew_membership(members)`
- `cancel_membership(members)`
- `calculate_fee(months, monthly_rate)`
- `display_members(members)`

The program should:

- Ask for the number of members to register initially.
- Store each member as a dictionary with a name, plan type, and active status, e.g. `{"name": "Kevin", "plan": "Standard", "active": True}`.
- Plan types and their monthly rates:
  - Basic: $20/month
  - Standard: $35/month
  - Premium: $50/month
- Display a menu:
  ```
  1. View All Members
  2. Renew Membership
  3. Cancel Membership
  4. View Active Members Count
  5. Exit
  ```

If a member renews:
- Ask for the member's name.
- Check if the member exists.
- Ask how many months they are renewing for.
- Calculate the fee (using `calculate_fee`, based on their plan's monthly rate).
- Mark the member as active.
- Display the amount charged.

If a member cancels:
- Check if the member exists.
- Mark the member as inactive (do not remove them from the list).

When viewing active members count, display how many members currently have active status.

Before exiting, display:
- Total number of members
- Number of active members
- Number of inactive members
- Total revenue collected from all renewals

## Concepts Tested
- Dictionaries
- Lists
- Functions
- Loops
- Conditional statements
- Booleans
- Variables
- User input
- List/dictionary manipulation