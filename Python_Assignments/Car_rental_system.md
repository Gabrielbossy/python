# Task 13: Car Rental System

## Problem Statement
A car rental company wants a program to manage its fleet, rentals, and returns.

## Requirements

Create the following functions:
- `add_car(cars)`
- `rent_car(cars, rentals)`
- `return_car(cars, rentals)`
- `calculate_cost(days, daily_rate)`
- `display_cars(cars)`

The program should:

- Ask for the number of cars in the fleet.
- Store each car as a dictionary with a plate number, category, and availability status, e.g. `{"plate": "KDB456Y", "category": "SUV", "available": True}`.
- Category daily rates:
  - Economy: $30/day
  - Sedan: $45/day
  - SUV: $70/day
- Display a menu:
  ```
  1. View All Cars
  2. Rent a Car
  3. Return a Car
  4. View Active Rentals
  5. Exit
  ```

If a customer rents a car:
- Show available cars.
- Ask for the plate number they want.
- Check the car exists and is available.
- Ask the customer's name.
- Ask how many days they will rent it for.
- Calculate the cost (using `calculate_cost`, based on the car's category rate).
- Mark the car as unavailable.
- Store the rental as a dictionary with plate, customer name, and days, and add it to `rentals`.
- Display the total cost.

If a customer returns a car:
- Ask for the plate number.
- Check if that car is currently rented.
- Mark the car as available again.
- Remove it from `rentals`.

When viewing active rentals, show the plate number, customer name, and days rented for each active rental.

Before exiting, display:
- Total number of cars in the fleet
- Number of cars currently available
- Number of cars currently rented out
- Total revenue generated from all rentals

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