"""
Inventory Stock Management System
-------------------------------------
A simple console-based program to manage product stock levels.
"""

LOW_STOCK_THRESHOLD = 5


def add_product(inventory):
    """Add a new product to the inventory."""
    name = input("Enter product name: ").strip()

    try:
        price = float(input(f"Enter price for {name}: "))
        if price < 0:
            print("Price cannot be negative.\n")
            return
    except ValueError:
        print("Invalid price. Please enter a number.\n")
        return

    try:
        quantity = int(input(f"Enter starting quantity for {name}: "))
        if quantity < 0:
            print("Quantity cannot be negative.\n")
            return
    except ValueError:
        print("Invalid quantity. Please enter a whole number.\n")
        return

    inventory.append({"name": name, "price": price, "quantity": quantity})
    print(f'"{name}" added with {quantity} units at ${price:.2f} each.\n')


def find_product(inventory, name):
    """Helper function to find a product by name (case-insensitive)."""
    for product in inventory:
        if product["name"].lower() == name.lower():
            return product
    return None


def sell_product(inventory):
    """Sell units of a product, reducing its stock. Returns the sale amount."""
    name = input("Enter the product name to sell: ").strip()
    product = find_product(inventory, name)

    if product is None:
        print(f'"{name}" was not found in inventory.\n')
        return 0

    try:
        quantity = int(input("Enter quantity to sell: "))
        if quantity <= 0:
            print("Quantity must be positive.\n")
            return 0
    except ValueError:
        print("Invalid quantity.\n")
        return 0

    if quantity > product["quantity"]:
        print(f"Not enough stock. Only {product['quantity']} units available.\n")
        return 0

    product["quantity"] -= quantity
    sale_amount = quantity * product["price"]
    print(f"Sold {quantity} unit(s) of {product['name']} for ${sale_amount:.2f}.\n")
    return sale_amount


def restock_product(inventory):
    """Add units back to a product's stock."""
    name = input("Enter the product name to restock: ").strip()
    product = find_product(inventory, name)

    if product is None:
        print(f'"{name}" was not found in inventory.\n')
        return

    try:
        quantity = int(input("Enter quantity to add: "))
        if quantity <= 0:
            print("Quantity must be positive.\n")
            return
    except ValueError:
        print("Invalid quantity.\n")
        return

    product["quantity"] += quantity
    print(f"Restocked {quantity} unit(s) of {product['name']}. New total: {product['quantity']}\n")


def display_inventory(inventory):
    """Display all products and their current stock."""
    print("\n--- Inventory ---")
    if not inventory:
        print("No products in inventory.")
    else:
        for product in inventory:
            print(
                f"{product['name']} - ${product['price']:.2f} - "
                f"{product['quantity']} in stock"
            )
    print("-----------------\n")


def low_stock_report(inventory, threshold):
    """Display products at or below the given stock threshold."""
    low_stock_items = [p for p in inventory if p["quantity"] <= threshold]

    print(f"\n--- Low Stock Report (threshold: {threshold}) ---")
    if not low_stock_items:
        print("No products are low on stock.")
    else:
        for product in low_stock_items:
            print(f"{product['name']} - only {product['quantity']} left!")
    print("---------------------------------------\n")


def display_summary(inventory, total_revenue):
    """Display the final summary before exiting."""
    total_products = len(inventory)
    total_units = sum(p["quantity"] for p in inventory)

    print("\n=== Inventory Summary ===")
    print(f"Total number of distinct products: {total_products}")
    print(f"Total units remaining: {total_units}")
    print(f"Total revenue generated: ${total_revenue:.2f}")
    print("==========================\n")


def main():
    inventory = []
    total_revenue = 0

    while True:
        try:
            num_products = int(input("Enter the number of products: "))
            if num_products <= 0:
                print("Please enter a positive number.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    print()
    for i in range(num_products):
        print(f"Product {i + 1}:")
        add_product(inventory)

    while True:
        print("Inventory Menu")
        print("1. View Inventory")
        print("2. Sell Product")
        print("3. Restock Product")
        print("4. Low Stock Report")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            display_inventory(inventory)
        elif choice == "2":
            total_revenue += sell_product(inventory)
        elif choice == "3":
            restock_product(inventory)
        elif choice == "4":
            low_stock_report(inventory, LOW_STOCK_THRESHOLD)
        elif choice == "5":
            display_summary(inventory, total_revenue)
            print("Thank you for using the Inventory Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.\n")


if __name__ == "__main__":
    main()