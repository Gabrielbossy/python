# Task 21: Movie Streaming Subscription Manager

## Problem Statement
A streaming service wants a program to manage subscriber accounts and monthly billing.

## Requirements

Create the following functions:
- `add_subscriber(subscribers)`
- `upgrade_plan(subscribers)`
- `cancel_subscription(subscribers)`
- `calculate_monthly_bill(subscribers)`
- `display_subscribers(subscribers)`

The program should:

- Ask for the number of subscribers to register initially.
- Store each subscriber as a dictionary with a name, plan, and active status, e.g. `{"name": "Leo", "plan": "Basic", "active": True}`.
- Plan monthly prices:
  - Basic: $8
  - Standard: $13
  - Premium: $18
- Display a menu:
  ```
  1. View All Subscribers
  2. Upgrade/Change Plan
  3. Cancel Subscription
  4. View Monthly Billing Report
  5. Exit
  ```

If a subscriber upgrades or changes their plan:
- Ask for the subscriber's name.
- Check the subscriber exists and is active.
- Show the available plans.
- Ask for the new plan.
- Validate it's one of the three valid plans.
- Update the subscriber's plan.

If a subscriber cancels:
- Ask for the subscriber's name.
- Check the subscriber exists.
- Mark them as inactive (do not remove them from the list).

When viewing the monthly billing report (using `calculate_monthly_bill`), show each **active** subscriber's name, plan, and monthly charge, along with the total revenue for the month.

Before exiting, display:
- Total number of subscribers
- Number of active subscribers
- Number of cancelled subscribers
- Total monthly revenue from active subscribers

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