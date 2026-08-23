"""
Coffee Shop Loyalty Program System
----------------------------------------
A simple console-based program to manage customers and a points-based
loyalty program.
"""

POINTS_PER_DOLLARS = 10  # 1 point earned for every $10 spent
REWARD_COST = 50  # points required to redeem a reward


def register_customer(customers):
    """Register a new loyalty program customer."""
    name = input("Enter customer name: ").strip()
    customers.append({"name": name, "points": 0, "total_spent": 0})
    print(f'"{name}" registered with 0 points.\n')


def find_customer(customers, name):
    """Helper function to find a customer by name (case-insensitive)."""
    for customer in customers:
        if customer["name"].lower() == name.lower():
            return customer
    return None


def calculate_points(amount_spent):
    """Calculate and return points earned for a given amount spent."""
    return int(amount_spent // POINTS_PER_DOLLARS)


def record_purchase(customers):
    """Record a purchase for a customer and award points."""
    name = input("Enter the customer's name: ").strip()
    customer = find_customer(customers, name)

    if customer is None:
        print(f'No customer named "{name}" was found.\n')
        return

    try:
        amount = float(input("Enter amount spent: "))
        if amount <= 0:
            print("Amount must be positive.\n")
            return
    except ValueError:
        print("Invalid amount.\n")
        return

    points_earned = calculate_points(amount)
    customer["points"] += points_earned
    customer["total_spent"] += amount

    print(f"{customer['name']} earned {points_earned} point(s) for this purchase.")
    print(f"New points balance: {customer['points']}\n")


def redeem_reward(customers):
    """Redeem a reward for a customer if they have enough points."""
    name = input("Enter the customer's name: ").strip()
    customer = find_customer(customers, name)

    if customer is None:
        print(f'No customer named "{name}" was found.\n')
        return

    if customer["points"] < REWARD_COST:
        print(
            f"{customer['name']} has only {customer['points']} point(s). "
            f"Need {REWARD_COST} to redeem a reward.\n"
        )
        return

    customer["points"] -= REWARD_COST
    print(f"Reward redeemed for {customer['name']}! Remaining points: {customer['points']}\n")


def display_customers(customers):
    """Display all customers, their points, and total spent."""
    print("\n--- Customers ---")
    if not customers:
        print("No customers registered yet.")
    else:
        for customer in customers:
            print(
                f"{customer['name']} - Points: {customer['points']} - "
                f"Total spent: ${customer['total_spent']:.2f}"
            )
    print("-----------------\n")


def display_top_customer(customers):
    """Find and display the customer who has spent the most."""
    customers_with_spending = [c for c in customers if c["total_spent"] > 0]

    if not customers_with_spending:
        print("No purchases have been recorded yet.\n")
        return

    top_customer = max(customers_with_spending, key=lambda c: c["total_spent"])
    print(
        f"\nTop customer: {top_customer['name']} - "
        f"${top_customer['total_spent']:.2f} spent\n"
    )


def display_summary(customers):
    """Display the final summary before exiting."""
    total_customers = len(customers)
    total_points = sum(c["points"] for c in customers)
    total_spent = sum(c["total_spent"] for c in customers)

    print("\n=== Loyalty Program Summary ===")
    print(f"Total number of customers: {total_customers}")
    print(f"Total points currently held: {total_points}")
    print(f"Total amount spent by all customers: ${total_spent:.2f}")

    if customers:
        top_spender = max(customers, key=lambda c: c["total_spent"])
        print(f"Top spender: {top_spender['name']} (${top_spender['total_spent']:.2f})")
    else:
        print("Top spender: N/A (no customers)")
    print("================================\n")


def main():
    customers = []

    while True:
        try:
            num_customers = int(input("Enter the number of customers to register: "))
            if num_customers <= 0:
                print("Please enter a positive number.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    print()
    for i in range(num_customers):
        register_customer(customers)

    while True:
        print("Loyalty Program Menu")
        print("1. View All Customers")
        print("2. Record a Purchase")
        print("3. Redeem Reward")
        print("4. View Top Customer")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            display_customers(customers)
        elif choice == "2":
            record_purchase(customers)
        elif choice == "3":
            redeem_reward(customers)
        elif choice == "4":
            display_top_customer(customers)
        elif choice == "5":
            display_summary(customers)
            print("Thank you for using the Coffee Shop Loyalty Program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.\n")


if __name__ == "__main__":
    main()