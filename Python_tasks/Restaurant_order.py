"""
Restaurant Order Management System
------------------------------------
A simple console-based program to manage customer orders from a menu.
"""


def add_menu_item(menu):
    """Add a new item to the restaurant's menu."""
    name = input("Enter item name: ").strip()
    try:
        price = float(input(f"Enter price for {name}: "))
        if price < 0:
            print("Price cannot be negative.\n")
            return
    except ValueError:
        print("Invalid price. Please enter a number.\n")
        return

    menu.append({"name": name, "price": price})
    print(f'"{name}" added to the menu at ${price:.2f}.\n')


def display_menu(menu):
    """Display all items currently on the menu."""
    print("\n--- Menu ---")
    if not menu:
        print("The menu is currently empty.")
    else:
        for item in menu:
            print(f"{item['name']} - ${item['price']:.2f}")
    print("------------\n")


def calculate_total(current_order):
    """Calculate and return the total price of the current order."""
    return sum(item["price"] for item in current_order)


def place_order(menu, current_order):
    """Add a menu item to the customer's current order."""
    if not menu:
        print("The menu is empty. Nothing to order.\n")
        return

    display_menu(menu)
    name = input("Enter the name of the item to order: ").strip()

    # Find the item on the menu (case-insensitive match)
    selected_item = None
    for item in menu:
        if item["name"].lower() == name.lower():
            selected_item = item
            break

    if selected_item is None:
        print(f'"{name}" is not on the menu.\n')
        return

    current_order.append(selected_item)
    print(f'Added "{selected_item["name"]}" to your order.\n')


def remove_from_order(current_order):
    """Remove an item from the customer's current order."""
    if not current_order:
        print("Your order is currently empty.\n")
        return

    name = input("Enter the name of the item to remove: ").strip()

    for item in current_order:
        if item["name"].lower() == name.lower():
            current_order.remove(item)
            print(f'Removed "{item["name"]}" from your order.\n')
            return

    print(f'"{name}" is not in your current order.\n')


def display_order(current_order):
    """Display the current order and running total."""
    print("\n--- Current Order ---")
    if not current_order:
        print("No items ordered yet.")
    else:
        for item in current_order:
            print(f"{item['name']} - ${item['price']:.2f}")
        total = calculate_total(current_order)
        print(f"Running Total: ${total:.2f}")
    print("----------------------\n")


def checkout(current_order):
    """Display the final receipt before exiting."""
    total = calculate_total(current_order)

    print("\n=== Final Receipt ===")
    if not current_order:
        print("No items were ordered.")
    else:
        for item in current_order:
            print(f"{item['name']} - ${item['price']:.2f}")
    print(f"\nNumber of items ordered: {len(current_order)}")
    print(f"Total Bill: ${total:.2f}")
    print("======================\n")


def main():
    menu = []
    current_order = []

    while True:
        try:
            num_items = int(input("Enter the number of menu items: "))
            if num_items <= 0:
                print("Please enter a positive number.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    print()
    for i in range(num_items):
        print(f"Menu Item {i + 1}:")
        add_menu_item(menu)

    while True:
        print("Restaurant Menu")
        print("1. View Menu")
        print("2. Add Item to Order")
        print("3. Remove Item from Order")
        print("4. View Current Order & Total")
        print("5. Checkout & Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            display_menu(menu)
        elif choice == "2":
            place_order(menu, current_order)
        elif choice == "3":
            remove_from_order(current_order)
        elif choice == "4":
            display_order(current_order)
        elif choice == "5":
            checkout(current_order)
            print("Thank you for dining with us. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.\n")


if __name__ == "__main__":
    main()