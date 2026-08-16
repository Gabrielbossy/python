# Task 14: Event Ticket Booking System

## Problem Statement
An events company wants a program to manage ticket sales for multiple events.

## Requirements

Create the following functions:
- `add_event(events)`
- `buy_ticket(events, sales)`
- `refund_ticket(events, sales)`
- `calculate_revenue(sales)`
- `display_events(events)`

The program should:

- Ask for the number of events.
- Store each event as a dictionary with a name, ticket price, and tickets available, e.g. `{"name": "Music Festival", "price": 500, "tickets_available": 100}`.
- Display a menu:
  ```
  1. View All Events
  2. Buy Ticket
  3. Refund Ticket
  4. View Sales Report
  5. Exit
  ```

If a customer buys a ticket:
- Show the events list.
- Ask for the event name.
- Check the event exists and has tickets available.
- Ask the customer's name.
- Ask how many tickets they want.
- Check enough tickets are available for the quantity requested.
- Subtract the quantity from `tickets_available`.
- Store the sale as a dictionary with event name, customer name, and quantity, and add it to `sales`.
- Display the amount charged.

If a customer requests a refund:
- Ask for the customer's name and event name.
- Check if a matching sale exists.
- Add the refunded quantity back to `tickets_available`.
- Remove the sale from `sales`.

When viewing the sales report, show every sale (event, customer, quantity) and the total revenue (using `calculate_revenue`).

Before exiting, display:
- Total number of events
- Total tickets sold (across all events, accounting for refunds)
- Total revenue generated
- The best-selling event (event with the most tickets sold)

## Concepts Tested
- Dictionaries
- Lists
- Functions
- Loops
- Conditional statements
- Variables
- User input
- List/dictionary manipulation