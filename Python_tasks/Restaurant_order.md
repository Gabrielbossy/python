# Task 5: Restaurant Order Management System

## Problem Statement
A restaurant wants a program to manage customer orders from its menu.

## Requirements

Create the following functions:
- `add_menu_item(menu)`
- `place_order(menu, current_order)`
- `remove_from_order(current_order)`
- `calculate_total(current_order)`
- `display_menu(menu)`

The program should:

- Ask for the number of menu items.
- Store each menu item as a dictionary with a name and price, e.g. `{"name": "Burger", "price": 250}`.
- Display a menu:
  ```
  1. View Menu
  2. Add Item to Order
  3. Remove Item from Order
  4. View Current Order & Total
  5. Checkout & Exit
  ```

If a customer adds an item to their order:
- Show the menu.
- Ask which item (by name).
- Check if it exists on the menu.
- Add it to the current order list.

If a customer removes an item:
- Check if it's in the current order.
- Remove it.

When viewing the order, show every item currently ordered and the running total (using `calculate_total`).

Before exiting (checkout):
- Display the final order list
- Display the total bill
- Display the number of items ordered

## Concepts Tested
- Dictionaries
- Lists
- Functions
- Loops
- Conditional statements
- Variables
- User input
- List/dictionary manipulation
