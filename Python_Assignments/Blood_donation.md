# Task 19: Blood Donation Center Management System

## Problem Statement
A blood donation center wants a program to manage blood stock by type and handle donations and requests.

## Requirements

Create the following functions:
- `initialize_stock(stock)`
- `record_donation(stock, donations)`
- `request_blood(stock, requests)`
- `display_stock(stock)`
- `low_stock_alert(stock, threshold)`

The program should:

- Initialize a stock dictionary covering these blood types: `A+`, `A-`, `B+`, `B-`, `AB+`, `AB-`, `O+`, `O-`, each starting at 0 units, e.g. `{"A+": 0, "A-": 0, ...}`.
- Display a menu:
  ```
  1. View Blood Stock
  2. Record a Donation
  3. Request Blood
  4. Low Stock Alert
  5. Exit
  ```

If a donation is recorded:
- Ask for the donor's name and blood type.
- Validate the blood type is one of the eight valid types.
- Ask how many units were donated.
- Add the units to that blood type's stock.
- Store the donation as a dictionary with donor name, blood type, and units, and add it to `donations`.

If blood is requested (e.g. for a patient/hospital):
- Ask for the requester's name and the blood type needed.
- Validate the blood type is valid.
- Ask how many units are needed.
- Check enough units are available in stock.
- Subtract the units from stock.
- Store the request as a dictionary with requester name, blood type, and units, and add it to `requests`.
- Display a confirmation message.

When viewing stock, display the units available for every blood type.

When checking the low stock alert, use a threshold (e.g. 5 units) and display every blood type at or below that threshold.

Before exiting, display:
- Total units of blood currently in stock (all types combined)
- Total number of donations recorded
- Total number of requests fulfilled
- The blood type with the highest stock

## Concepts Tested
- Dictionaries
- Lists
- Functions
- Loops
- Conditional statements
- Variables
- User input
- Dictionary manipulation