# Task 17: Package Delivery Tracking System

## Problem Statement
A courier company wants a program to track packages from pickup to delivery.

## Requirements

Create the following functions:
- `add_package(packages)`
- `assign_driver(packages)`
- `mark_delivered(packages)`
- `calculate_fee(distance_km, rate_per_km)`
- `display_packages(packages)`

The program should:

- Ask for the number of packages to log.
- Store each package as a dictionary with a tracking ID, recipient name, distance (in km), driver (starts as `None`), and status (starts as `"Pending"`), e.g. `{"id": "PKG001", "recipient": "Grace", "distance": 12, "driver": None, "status": "Pending"}`.
- Tracking IDs should be generated automatically, e.g. `PKG001`, `PKG002`, `PKG003`.
- Display a menu:
  ```
  1. View All Packages
  2. Assign Driver
  3. Mark as Delivered
  4. View Delivery Fee Report
  5. Exit
  ```

If a driver is assigned:
- Ask for the tracking ID.
- Check the package exists and its status is `"Pending"`.
- Ask for the driver's name.
- Store the driver's name on the package.
- Update its status to `"In Transit"`.

If a package is marked as delivered:
- Ask for the tracking ID.
- Check the package exists and its status is `"In Transit"`.
- Update its status to `"Delivered"`.
- Calculate the delivery fee (using `calculate_fee`, with a fixed rate of $1.50/km).
- Display the fee.

When viewing the delivery fee report, show every **delivered** package's tracking ID, recipient, distance, and fee charged, along with the total fees collected.

Before exiting, display:
- Total number of packages
- Number of packages still pending
- Number of packages in transit
- Number of packages delivered
- Total delivery fees collected

## Concepts Tested
- Dictionaries
- Lists
- Functions
- Loops
- Conditional statements
- Variables
- User input
- List/dictionary manipulation