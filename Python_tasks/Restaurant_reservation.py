"""
Restaurant Table Reservation System
------------------------------------------
A simple console-based program to manage table reservations.
"""

DEPOSIT_RATE_PER_PERSON = 5


def add_table(tables):
    """Add a new table with a seating capacity."""
    try:
        capacity = int(input("Enter seating capacity for this table: "))
        if capacity <= 0:
            print("Capacity must be a positive number.\n")
            return
    except ValueError:
        print("Invalid capacity. Please enter a whole number.\n")
        return

    table_number = len(tables) + 1
    tables.append({"table_number": table_number, "capacity": capacity, "status": "Free"})
    print(f"Table {table_number} added with a capacity of {capacity}.\n")


def find_table(tables, table_number):
    """Helper function to find a table by its number."""
    for table in tables:
        if table["table_number"] == table_number:
            return table
    return None


def calculate_deposit(party_size, rate_per_person):
    """Calculate and return the deposit required for a party size."""
    return party_size * rate_per_person


def display_tables(tables):
    """Display all tables and their current status."""
    print("\n--- Tables ---")
    if not tables:
        print("No tables have been added yet.")
    else:
        for table in tables:
            print(
                f"Table {table['table_number']} - Capacity {table['capacity']} - "
                f"Status: {table['status']}"
            )
    print("--------------\n")


def reserve_table(tables, reservations):
    """Reserve a free table for a customer. Returns the deposit charged."""
    free_tables = [t for t in tables if t["status"] == "Free"]

    if not free_tables:
        print("No free tables available.\n")
        return 0

    print("\n--- Free Tables ---")
    for table in free_tables:
        print(f"Table {table['table_number']} - Capacity {table['capacity']}")
    print("--------------------\n")

    try:
        table_number = int(input("Enter the table number to reserve: "))
    except ValueError:
        print("Invalid table number.\n")
        return 0

    table = find_table(tables, table_number)

    if table is None:
        print(f"No table found with number {table_number}.\n")
        return 0

    if table["status"] != "Free":
        print(f"Table {table_number} is not free.\n")
        return 0

    customer_name = input("Enter customer name: ").strip()

    try:
        party_size = int(input("Enter party size: "))
        if party_size <= 0:
            print("Party size must be a positive number.\n")
            return 0
    except ValueError:
        print("Invalid party size.\n")
        return 0

    if party_size > table["capacity"]:
        print(f"Party size exceeds table capacity ({table['capacity']}).\n")
        return 0

    deposit = calculate_deposit(party_size, DEPOSIT_RATE_PER_PERSON)

    table["status"] = "Reserved"
    reservations.append({
        "table_number": table_number,
        "customer": customer_name,
        "party_size": party_size,
        "deposit": deposit,
    })

    print(f"Table {table_number} reserved for {customer_name} (party of {party_size}).")
    print(f"Deposit charged: ${deposit}\n")
    return deposit


def cancel_reservation(tables, reservations):
    """Cancel a reservation and free up the table."""
    try:
        table_number = int(input("Enter the table number to cancel: "))
    except ValueError:
        print("Invalid table number.\n")
        return

    table = find_table(tables, table_number)

    if table is None:
        print(f"No table found with number {table_number}.\n")
        return

    if table["status"] != "Reserved":
        print(f"Table {table_number} does not have an active reservation.\n")
        return

    table["status"] = "Free"

    for reservation in reservations:
        if reservation["table_number"] == table_number:
            reservations.remove(reservation)
            break

    print(f"Reservation for table {table_number} has been cancelled.\n")


def display_reservations(reservations):
    """Display all active reservations."""
    print("\n--- Active Reservations ---")
    if not reservations:
        print("No active reservations.")
    else:
        for reservation in reservations:
            print(
                f"Table {reservation['table_number']} - {reservation['customer']} - "
                f"Party of {reservation['party_size']} - Deposit: ${reservation['deposit']}"
            )
    print("----------------------------\n")


def display_summary(tables, reservations):
    """Display the final summary before exiting."""
    total_tables = len(tables)
    free_count = sum(1 for t in tables if t["status"] == "Free")
    reserved_count = total_tables - free_count
    total_deposits = sum(r["deposit"] for r in reservations)

    print("\n=== Reservation Summary ===")
    print(f"Total number of tables: {total_tables}")
    print(f"Tables currently free: {free_count}")
    print(f"Tables currently reserved: {reserved_count}")
    print(f"Total deposits collected: ${total_deposits}")
    print("============================\n")


def main():
    tables = []
    reservations = []

    while True:
        try:
            num_tables = int(input("Enter the number of tables: "))
            if num_tables <= 0:
                print("Please enter a positive number.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    print()
    for i in range(num_tables):
        print(f"Table {i + 1}:")
        add_table(tables)

    while True:
        print("Reservation Menu")
        print("1. View All Tables")
        print("2. Reserve a Table")
        print("3. Cancel a Reservation")
        print("4. View Active Reservations")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            display_tables(tables)
        elif choice == "2":
            reserve_table(tables, reservations)
        elif choice == "3":
            cancel_reservation(tables, reservations)
        elif choice == "4":
            display_reservations(reservations)
        elif choice == "5":
            display_summary(tables, reservations)
            print("Thank you for using the Restaurant Reservation System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.\n")


if __name__ == "__main__":
    main()