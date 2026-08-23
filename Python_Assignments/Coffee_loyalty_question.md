# Task 16: Coffee Shop Loyalty Program System

## Problem Statement
A coffee shop wants a program to manage customer purchases and a points-based loyalty program.

## Requirements

Create the following functions:
- `register_customer(customers)`
- `record_purchase(customers)`
- `redeem_reward(customers)`
- `calculate_points(amount_spent)`
- `display_customers(customers)`

The program should:

- Ask for the number of customers to register initially.
- Store each customer as a dictionary with a name, points balance, and total spent, e.g. `{"name": "Diana", "points": 0, "total_spent": 0}`.
- Display a menu:
  ```
  1. View All Customers
  2. Record a Purchase
  3. Redeem Reward
  4. View Top Customer
  5. Exit
  ```

If a purchase is recorded:
- Ask for the customer's name.
- Check the customer exists.
- Ask for the amount spent.
- Calculate points earned (using `calculate_points` — 1 point for every $10 spent, rounded down).
- Add the points to the customer's balance.
- Add the amount to the customer's total spent.
- Display the points earned.

If a customer redeems a reward:
- Ask for the customer's name.
- Check the customer exists.
- A reward costs 50 points.
- Check the customer has enough points.
- Subtract 50 points from their balance.
- Display a confirmation message.

When viewing the top customer, find whichever customer has spent the most in total.

Before exiting, display:
- Total number of customers
- Total points currently held across all customers
- Total amount spent by all customers combined
- The top spender

## Concepts Tested
- Dictionaries
- Lists
- Functions
- Loops
- Conditional statements
- Variables
- User input
- List/dictionary manipulation