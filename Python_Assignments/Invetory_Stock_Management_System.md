# Task 8: Inventory Stock Management System

## Problem Statement
A retail shop wants a program to manage its product stock levels.

## Requirements

Create the following functions:
- `add_product(inventory)`
- `sell_product(inventory)`
- `restock_product(inventory)`
- `display_inventory(inventory)`
- `low_stock_report(inventory, threshold)`

The program should:

- Ask for the number of products.
- Store each product as a dictionary with a name, price, and quantity in stock, e.g. `{"name": "Notebook", "price": 50, "quantity": 20}`.
- Display a menu:
  ```
  1. View Inventory
  2. Sell Product
  3. Restock Product
  4. Low Stock Report
  5. Exit
  ```

If a user sells a product:
- Ask for the product name.
- Check if it exists in the inventory.
- Ask how many units are being sold.
- Validate there is enough stock available.
- Subtract the quantity sold from stock.
- Display the sale amount (quantity × price).

If a user restocks a product:
- Ask for the product name.
- Check if it exists in the inventory.
- Ask how many units are being added.
- Add the quantity to the current stock.

If a user requests a low stock report:
- Use a threshold value (e.g. 5 units).
- Display every product whose quantity is at or below the threshold.

Before exiting, display:
- Total number of distinct products
- Total number of units remaining across all products
- Total revenue generated from all sales

## Concepts Tested
- Dictionaries
- Lists
- Functions
- Loops
- Conditional statements
- Variables
- User input
- List/dictionary manipulation
