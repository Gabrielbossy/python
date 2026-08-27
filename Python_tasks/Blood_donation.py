"""
Blood Donation Center Management System
----------------------------------------------
A simple console-based program to manage blood stock, donations, and requests.
"""

VALID_BLOOD_TYPES = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
LOW_STOCK_THRESHOLD = 5


def initialize_stock(stock):
    """Initialize the stock dictionary with 0 units for every blood type."""
    for blood_type in VALID_BLOOD_TYPES:
        stock[blood_type] = 0


def display_stock(stock):
    """Display units available for every blood type."""
    print("\n--- Blood Stock ---")
    for blood_type, units in stock.items():
        print(f"{blood_type}: {units} unit(s)")
    print("--------------------\n")


def record_donation(stock, donations):
    """Record a blood donation and add the units to stock."""
    donor_name = input("Enter donor's name: ").strip()
    blood_type = input("Enter blood type (e.g. A+, O-): ").strip().upper()

    if blood_type not in VALID_BLOOD_TYPES:
        print(f'"{blood_type}" is not a valid blood type.\n')
        return

    try:
        units = int(input("Enter units donated: "))
        if units <= 0:
            print("Units must be a positive number.\n")
            return
    except ValueError:
        print("Invalid number of units.\n")
        return

    stock[blood_type] += units
    donations.append({"donor": donor_name, "blood_type": blood_type, "units": units})

    print(f"Recorded {units} unit(s) of {blood_type} from {donor_name}.")
    print(f"New {blood_type} stock: {stock[blood_type]} unit(s)\n")


def request_blood(stock, requests):
    """Fulfill a blood request if enough stock is available."""
    requester_name = input("Enter requester's name: ").strip()
    blood_type = input("Enter blood type needed (e.g. A+, O-): ").strip().upper()

    if blood_type not in VALID_BLOOD_TYPES:
        print(f'"{blood_type}" is not a valid blood type.\n')
        return

    try:
        units = int(input("Enter units needed: "))
        if units <= 0:
            print("Units must be a positive number.\n")
            return
    except ValueError:
        print("Invalid number of units.\n")
        return

    if units > stock[blood_type]:
        print(f"Not enough {blood_type} in stock. Only {stock[blood_type]} unit(s) available.\n")
        return

    stock[blood_type] -= units
    requests.append({"requester": requester_name, "blood_type": blood_type, "units": units})

    print(f"Request fulfilled: {units} unit(s) of {blood_type} for {requester_name}.")
    print(f"Remaining {blood_type} stock: {stock[blood_type]} unit(s)\n")


def low_stock_alert(stock, threshold):
    """Display every blood type at or below the given threshold."""
    print(f"\n--- Low Stock Alert (threshold: {threshold}) ---")
    low_types = {bt: units for bt, units in stock.items() if units <= threshold}

    if not low_types:
        print("No blood types are currently low on stock.")
    else:
        for blood_type, units in low_types.items():
            print(f"{blood_type}: only {units} unit(s) left!")
    print("--------------------------------------------\n")


def display_summary(stock, donations, requests):
    """Display the final summary before exiting."""
    total_units = sum(stock.values())
    total_donations = len(donations)
    total_requests = len(requests)
    highest_type = max(stock, key=stock.get)

    print("\n=== Blood Bank Summary ===")
    print(f"Total units in stock (all types): {total_units}")
    print(f"Total donations recorded: {total_donations}")
    print(f"Total requests fulfilled: {total_requests}")
    print(f"Highest stocked type: {highest_type} ({stock[highest_type]} unit(s))")
    print("===========================\n")


def main():
    stock = {}
    initialize_stock(stock)
    donations = []
    requests = []

    while True:
        print("Blood Bank Menu")
        print("1. View Blood Stock")
        print("2. Record a Donation")
        print("3. Request Blood")
        print("4. Low Stock Alert")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            display_stock(stock)
        elif choice == "2":
            record_donation(stock, donations)
        elif choice == "3":
            request_blood(stock, requests)
        elif choice == "4":
            low_stock_alert(stock, LOW_STOCK_THRESHOLD)
        elif choice == "5":
            display_summary(stock, donations, requests)
            print("Thank you for using the Blood Donation Center System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.\n")


if __name__ == "__main__":
    main()