"""
Gym Membership Management System
-------------------------------------
A simple console-based program to manage gym members and payments.
"""

PLAN_RATES = {
    "basic": 20,
    "standard": 35,
    "premium": 50,
}


def register_member(members):
    """Register a new gym member with a chosen plan."""
    name = input("Enter member name: ").strip()

    print(f"Available plans: {', '.join(p.title() for p in PLAN_RATES)}")
    plan = input("Enter plan type: ").strip().lower()

    if plan not in PLAN_RATES:
        print(f'"{plan}" is not a valid plan. Member not registered.\n')
        return

    members.append({"name": name, "plan": plan.title(), "active": True})
    print(f'"{name}" registered on the {plan.title()} plan.\n')


def find_member(members, name):
    """Helper function to find a member by name (case-insensitive)."""
    for member in members:
        if member["name"].lower() == name.lower():
            return member
    return None


def calculate_fee(months, monthly_rate):
    """Calculate and return the total fee for a number of months."""
    return months * monthly_rate


def renew_membership(members):
    """Renew a member's plan for a given number of months. Returns fee charged."""
    name = input("Enter the member's name: ").strip()
    member = find_member(members, name)

    if member is None:
        print(f'No member named "{name}" was found.\n')
        return 0

    try:
        months = int(input("Enter number of months to renew: "))
        if months <= 0:
            print("Months must be a positive number.\n")
            return 0
    except ValueError:
        print("Invalid number of months.\n")
        return 0

    monthly_rate = PLAN_RATES[member["plan"].lower()]
    fee = calculate_fee(months, monthly_rate)

    member["active"] = True
    print(f"{member['name']}'s membership renewed for {months} month(s). Charged: ${fee}\n")
    return fee


def cancel_membership(members):
    """Mark a member's status as inactive."""
    name = input("Enter the member's name: ").strip()
    member = find_member(members, name)

    if member is None:
        print(f'No member named "{name}" was found.\n')
        return

    member["active"] = False
    print(f"{member['name']}'s membership has been cancelled.\n")


def display_members(members):
    """Display all members, their plan, and their active status."""
    print("\n--- Members ---")
    if not members:
        print("No members registered yet.")
    else:
        for member in members:
            status = "Active" if member["active"] else "Inactive"
            print(f"{member['name']} - {member['plan']} - {status}")
    print("---------------\n")


def display_active_count(members):
    """Display how many members are currently active."""
    active_count = sum(1 for member in members if member["active"])
    print(f"\nActive members: {active_count}\n")


def display_summary(members, total_revenue):
    """Display the final summary before exiting."""
    total_members = len(members)
    active_count = sum(1 for member in members if member["active"])
    inactive_count = total_members - active_count

    print("\n=== Gym Summary ===")
    print(f"Total number of members: {total_members}")
    print(f"Active members: {active_count}")
    print(f"Inactive members: {inactive_count}")
    print(f"Total revenue collected: ${total_revenue}")
    print("====================\n")


def main():
    members = []
    total_revenue = 0

    while True:
        try:
            num_members = int(input("Enter the number of members to register: "))
            if num_members <= 0:
                print("Please enter a positive number.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    print()
    for i in range(num_members):
        print(f"Member {i + 1}:")
        register_member(members)

    while True:
        print("Gym Menu")
        print("1. View All Members")
        print("2. Renew Membership")
        print("3. Cancel Membership")
        print("4. View Active Members Count")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            display_members(members)
        elif choice == "2":
            total_revenue += renew_membership(members)
        elif choice == "3":
            cancel_membership(members)
        elif choice == "4":
            display_active_count(members)
        elif choice == "5":
            display_summary(members, total_revenue)
            print("Thank you for using the Gym Membership System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.\n")


if __name__ == "__main__":
    main()