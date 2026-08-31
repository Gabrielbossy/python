# Task 23: Customer Support Ticket Queue System

## Problem Statement
A company's support desk wants a program to manage incoming tickets on a **first-come, first-served** basis.

## Requirements

Create the following functions:
- `submit_ticket(queue, ticket_counter)`
- `resolve_next_ticket(queue, resolved_tickets)`
- `view_queue(queue)`
- `average_wait_position(queue)`

The program should:

- Start with an empty queue (a list) and an empty list of resolved tickets.
- Store each ticket as a dictionary with a ticket ID, customer name, and issue description, e.g. `{"ticket_id": 1, "customer": "Zoe", "issue": "Login not working"}`.
- Ticket IDs should auto-increment starting from 1.
- Display a menu:
  ```
  1. Submit New Ticket
  2. Resolve Next Ticket
  3. View Queue
  4. View Resolved Tickets
  5. Exit
  ```

If a new ticket is submitted:
- Ask for the customer's name and a short issue description.
- Create the ticket and **add it to the end of the queue** (tickets must be handled in the order they arrive).

If the next ticket is resolved:
- Check the queue isn't empty.
- **Remove the ticket from the front of the queue** (not the end — this is the key rule of a queue).
- Add it to `resolved_tickets`.
- Display which ticket was resolved.

When viewing the queue, show every ticket currently waiting, in order, along with its position number (1st in line, 2nd in line, etc.).

`average_wait_position(queue)` should calculate and return the average position of all tickets currently in the queue (e.g. if there are 3 tickets, positions are 1, 2, 3, so the average is 2). This does not need a menu option on its own — call it from within the "View Queue" option to show alongside the list.

Before exiting, display:
- Total tickets ever submitted (queue + resolved combined)
- Number of tickets resolved
- Number of tickets still waiting in queue
- The very first unresolved ticket still waiting (if any)

## Concepts Tested
- Lists (used as a queue / FIFO structure)
- Dictionaries
- Functions
- Loops
- Conditional statements
- Variables
- User input
- List manipulation (`append` vs. removing from the front)