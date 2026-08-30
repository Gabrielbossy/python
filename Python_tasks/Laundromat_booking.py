"""
Laundromat Machine Booking System
----------------------------------------
A simple console-based program to manage washer/dryer bookings and payments.
"""

RATES_PER_MINUTE = {
    "washer": 0.10,
    "dryer": 0.08,
}


def add_machine(machines):
    """Add a new machine to the laundromat."""
    machine_type = input("Enter machine type (Washer/Dryer): ").strip().lower()

    if machine_type not in RATES_PER_MINUTE:
        print(f'"{machine_type}" is not a valid machine type.\n')
        return

    machine_id = len(machines) + 1
    machines.append({"machine_id": machine_id, "type": machine_type.title(), "status": "Free"})
    print(f"Machine {machine_id} ({machine_type.title()}) added.\n")


def find_machine(machines, machine_id):
    """Helper function to find a machine by its ID."""
    for machine in machines:
        if machine["machine_id"] == machine_id:
            return machine
    return None


def calculate_charge(minutes, rate_per_minute):
    """Calculate and return the charge for a cycle."""
    return minutes * rate_per_minute


def display_machines(machines):
    """Display all machines and their current status."""
    print("\n--- Machines ---")
    if not machines:
        print("No machines have been added yet.")
    else:
        for machine in machines:
            print(
                f"Machine {machine['machine_id']} - {machine['type']} - "
                f"{machine['status']}"
            )
    print("----------------\n")


def start_cycle(machines, sessions):
    """Start a cycle on a free machine."""
    free_machines = [m for m in machines if m["status"] == "Free"]

    if not free_machines:
        print("No machines are currently free.\n")
        return

    print("\n--- Free Machines ---")
    for machine in free_machines:
        print(f"Machine {machine['machine_id']} - {machine['type']}")
    print("----------------------\n")

    try:
        machine_id = int(input("Enter the machine ID to use: "))
    except ValueError:
        print("Invalid machine ID.\n")
        return

    machine = find_machine(machines, machine_id)

    if machine is None:
        print(f"No machine found with ID {machine_id}.\n")
        return

    if machine["status"] != "Free":
        print(f"Machine {machine_id} is not free.\n")
        return

    customer_name = input("Enter customer name: ").strip()

    machine["status"] = "In Use"
    sessions.append({
        "machine_id": machine_id,
        "customer": customer_name,
        "type": machine["type"],
    })

    print(f"Cycle started on Machine {machine_id} ({machine['type']}) for {customer_name}.\n")


def end_cycle(machines, sessions):
    """End a cycle, calculate the charge, and free up the machine."""
    try:
        machine_id = int(input("Enter the machine ID to end: "))
    except ValueError:
        print("Invalid machine ID.\n")
        return 0

    machine = find_machine(machines, machine_id)

    if machine is None:
        print(f"No machine found with ID {machine_id}.\n")
        return 0

    if machine["status"] != "In Use":
        print(f"Machine {machine_id} is not currently in use.\n")
        return 0

    try:
        minutes = float(input("Enter how many minutes the cycle ran: "))
        if minutes <= 0:
            print("Minutes must be a positive number.\n")
            return 0
    except ValueError:
        print("Invalid number of minutes.\n")
        return 0

    rate = RATES_PER_MINUTE[machine["type"].lower()]
    charge = calculate_charge(minutes, rate)

    machine["status"] = "Free"

    for session in sessions:
        if session["machine_id"] == machine_id:
            sessions.remove(session)
            break

    print(f"Cycle ended on Machine {machine_id}. Charge: ${charge:.2f}\n")
    return charge


def display_sessions(sessions):
    """Display all active sessions."""
    print("\n--- Active Sessions ---")
    if not sessions:
        print("No machines are currently in use.")
    else:
        for session in sessions:
            print(
                f"Machine {session['machine_id']} - {session['customer']} - "
                f"{session['type']}"
            )
    print("------------------------\n")


def display_summary(machines, total_revenue):
    """Display the final summary before exiting."""
    total_machines = len(machines)
    free_count = sum(1 for m in machines if m["status"] == "Free")
    in_use_count = total_machines - free_count

    print("\n=== Laundromat Summary ===")
    print(f"Total number of machines: {total_machines}")
    print(f"Machines currently free: {free_count}")
    print(f"Machines currently in use: {in_use_count}")
    print(f"Total revenue collected: ${total_revenue:.2f}")
    print("===========================\n")


def main():
    machines = []
    sessions = []
    total_revenue = 0

    while True:
        try:
            num_machines = int(input("Enter the number of machines: "))
            if num_machines <= 0:
                print("Please enter a positive number.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    print()
    for i in range(num_machines):
        print(f"Machine {i + 1}:")
        add_machine(machines)

    while True:
        print("Laundromat Menu")
        print("1. View All Machines")
        print("2. Start a Cycle")
        print("3. End a Cycle")
        print("4. View Active Sessions")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            display_machines(machines)
        elif choice == "2":
            start_cycle(machines, sessions)
        elif choice == "3":
            total_revenue += end_cycle(machines, sessions)
        elif choice == "4":
            display_sessions(sessions)
        elif choice == "5":
            display_summary(machines, total_revenue)
            print("Thank you for using the Laundromat Booking System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.\n")


if __name__ == "__main__":
    main()