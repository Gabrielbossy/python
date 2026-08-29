"""
Movie Streaming Subscription Manager
----------------------------------------------
A simple console-based program to manage streaming subscribers and billing.
"""

PLAN_PRICES = {
    "basic": 8,
    "standard": 13,
    "premium": 18,
}


def add_subscriber(subscribers):
    """Register a new subscriber with a chosen plan."""
    name = input("Enter subscriber name: ").strip()

    print(f"Available plans: {', '.join(p.title() for p in PLAN_PRICES)}")
    plan = input("Enter plan: ").strip().lower()

    if plan not in PLAN_PRICES:
        print(f'"{plan}" is not a valid plan. Subscriber not added.\n')
        return

    subscribers.append({"name": name, "plan": plan.title(), "active": True})
    print(f'"{name}" subscribed to the {plan.title()} plan.\n')


def find_subscriber(subscribers, name):
    """Helper function to find a subscriber by name (case-insensitive)."""
    for subscriber in subscribers:
        if subscriber["name"].lower() == name.lower():
            return subscriber
    return None


def upgrade_plan(subscribers):
    """Change an active subscriber's plan."""
    name = input("Enter the subscriber's name: ").strip()
    subscriber = find_subscriber(subscribers, name)

    if subscriber is None:
        print(f'No subscriber named "{name}" was found.\n')
        return

    if not subscriber["active"]:
        print(f'{subscriber["name"]}\'s subscription is cancelled and cannot be changed.\n')
        return

    print(f"Current plan: {subscriber['plan']}")
    print(f"Available plans: {', '.join(p.title() for p in PLAN_PRICES)}")
    new_plan = input("Enter the new plan: ").strip().lower()

    if new_plan not in PLAN_PRICES:
        print(f'"{new_plan}" is not a valid plan.\n')
        return

    subscriber["plan"] = new_plan.title()
    print(f"{subscriber['name']}'s plan updated to {subscriber['plan']}.\n")


def cancel_subscription(subscribers):
    """Mark a subscriber's status as inactive."""
    name = input("Enter the subscriber's name: ").strip()
    subscriber = find_subscriber(subscribers, name)

    if subscriber is None:
        print(f'No subscriber named "{name}" was found.\n')
        return

    subscriber["active"] = False
    print(f"{subscriber['name']}'s subscription has been cancelled.\n")


def calculate_monthly_bill(subscribers):
    """Calculate and return the total monthly revenue from active subscribers."""
    total = 0
    for subscriber in subscribers:
        if subscriber["active"]:
            total += PLAN_PRICES[subscriber["plan"].lower()]
    return total


def display_subscribers(subscribers):
    """Display all subscribers, their plan, and their active status."""
    print("\n--- Subscribers ---")
    if not subscribers:
        print("No subscribers registered yet.")
    else:
        for subscriber in subscribers:
            status = "Active" if subscriber["active"] else "Cancelled"
            print(f"{subscriber['name']} - {subscriber['plan']} - {status}")
    print("-------------------\n")


def display_billing_report(subscribers):
    """Display each active subscriber's monthly charge and the total revenue."""
    active_subscribers = [s for s in subscribers if s["active"]]

    print("\n--- Monthly Billing Report ---")
    if not active_subscribers:
        print("No active subscribers to bill.")
    else:
        for subscriber in active_subscribers:
            charge = PLAN_PRICES[subscriber["plan"].lower()]
            print(f"{subscriber['name']} - {subscriber['plan']} - ${charge}")
        total_revenue = calculate_monthly_bill(subscribers)
        print(f"\nTotal monthly revenue: ${total_revenue}")
    print("-------------------------------\n")


def display_summary(subscribers):
    """Display the final summary before exiting."""
    total_subscribers = len(subscribers)
    active_count = sum(1 for s in subscribers if s["active"])
    cancelled_count = total_subscribers - active_count
    total_revenue = calculate_monthly_bill(subscribers)

    print("\n=== Subscription Summary ===")
    print(f"Total number of subscribers: {total_subscribers}")
    print(f"Active subscribers: {active_count}")
    print(f"Cancelled subscribers: {cancelled_count}")
    print(f"Total monthly revenue: ${total_revenue}")
    print("=============================\n")


def main():
    subscribers = []

    while True:
        try:
            num_subscribers = int(input("Enter the number of subscribers to register: "))
            if num_subscribers <= 0:
                print("Please enter a positive number.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    print()
    for i in range(num_subscribers):
        print(f"Subscriber {i + 1}:")
        add_subscriber(subscribers)

    while True:
        print("Streaming Subscription Menu")
        print("1. View All Subscribers")
        print("2. Upgrade/Change Plan")
        print("3. Cancel Subscription")
        print("4. View Monthly Billing Report")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            display_subscribers(subscribers)
        elif choice == "2":
            upgrade_plan(subscribers)
        elif choice == "3":
            cancel_subscription(subscribers)
        elif choice == "4":
            display_billing_report(subscribers)
        elif choice == "5":
            display_summary(subscribers)
            print("Thank you for using the Streaming Subscription Manager. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.\n")


if __name__ == "__main__":
    main()