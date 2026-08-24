"""
Package Delivery Tracking System
--------------------------------------
A simple console-based program to track packages from pickup to delivery.
"""

RATE_PER_KM = 1.50


def add_package(packages):
    """Add a new package with an auto-generated tracking ID."""
    recipient = input("Enter recipient name: ").strip()

    try:
        distance = float(input("Enter distance to deliver (km): "))
        if distance < 0:
            print("Distance cannot be negative.\n")
            return
    except ValueError:
        print("Invalid distance. Please enter a number.\n")
        return

    tracking_id = f"PKG{len(packages) + 1:03d}"

    packages.append({
        "id": tracking_id,
        "recipient": recipient,
        "distance": distance,
        "driver": None,
        "status": "Pending",
    })
    print(f"Package {tracking_id} logged for {recipient} ({distance} km).\n")


def find_package(packages, tracking_id):
    """Helper function to find a package by tracking ID (case-insensitive)."""
    for package in packages:
        if package["id"].lower() == tracking_id.lower():
            return package
    return None


def calculate_fee(distance_km, rate_per_km):
    """Calculate and return the delivery fee for a given distance."""
    return distance_km * rate_per_km


def assign_driver(packages):
    """Assign a driver to a pending package and mark it In Transit."""
    tracking_id = input("Enter the tracking ID: ").strip()
    package = find_package(packages, tracking_id)

    if package is None:
        print(f"No package found with ID {tracking_id}.\n")
        return

    if package["status"] != "Pending":
        print(f"Package {package['id']} is not pending (status: {package['status']}).\n")
        return

    driver_name = input("Enter driver's name: ").strip()
    package["driver"] = driver_name
    package["status"] = "In Transit"

    print(f"Driver {driver_name} assigned to package {package['id']}. Status: In Transit.\n")


def mark_delivered(packages):
    """Mark an in-transit package as delivered and calculate its fee."""
    tracking_id = input("Enter the tracking ID: ").strip()
    package = find_package(packages, tracking_id)

    if package is None:
        print(f"No package found with ID {tracking_id}.\n")
        return

    if package["status"] != "In Transit":
        print(f"Package {package['id']} is not in transit (status: {package['status']}).\n")
        return

    package["status"] = "Delivered"
    fee = calculate_fee(package["distance"], RATE_PER_KM)

    print(f"Package {package['id']} delivered to {package['recipient']}.")
    print(f"Delivery fee: ${fee:.2f}\n")


def display_packages(packages):
    """Display all packages and their current status."""
    print("\n--- Packages ---")
    if not packages:
        print("No packages logged yet.")
    else:
        for package in packages:
            driver = package["driver"] if package["driver"] else "Unassigned"
            print(
                f"{package['id']} - {package['recipient']} - {package['distance']} km - "
                f"Driver: {driver} - Status: {package['status']}"
            )
    print("----------------\n")


def display_fee_report(packages):
    """Display all delivered packages, their fees, and the total collected."""
    delivered = [p for p in packages if p["status"] == "Delivered"]

    print("\n--- Delivery Fee Report ---")
    if not delivered:
        print("No packages have been delivered yet.")
    else:
        total_fees = 0
        for package in delivered:
            fee = calculate_fee(package["distance"], RATE_PER_KM)
            total_fees += fee
            print(
                f"{package['id']} - {package['recipient']} - "
                f"{package['distance']} km - ${fee:.2f}"
            )
        print(f"\nTotal fees collected: ${total_fees:.2f}")
    print("----------------------------\n")


def display_summary(packages):
    """Display the final summary before exiting."""
    total_packages = len(packages)
    pending_count = sum(1 for p in packages if p["status"] == "Pending")
    in_transit_count = sum(1 for p in packages if p["status"] == "In Transit")
    delivered_count = sum(1 for p in packages if p["status"] == "Delivered")
    total_fees = sum(
        calculate_fee(p["distance"], RATE_PER_KM)
        for p in packages if p["status"] == "Delivered"
    )

    print("\n=== Delivery Summary ===")
    print(f"Total number of packages: {total_packages}")
    print(f"Packages still pending: {pending_count}")
    print(f"Packages in transit: {in_transit_count}")
    print(f"Packages delivered: {delivered_count}")
    print(f"Total delivery fees collected: ${total_fees:.2f}")
    print("=========================\n")


def main():
    packages = []

    while True:
        try:
            num_packages = int(input("Enter the number of packages to log: "))
            if num_packages <= 0:
                print("Please enter a positive number.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    print()
    for i in range(num_packages):
        print(f"Package {i + 1}:")
        add_package(packages)

    while True:
        print("Delivery Tracking Menu")
        print("1. View All Packages")
        print("2. Assign Driver")
        print("3. Mark as Delivered")
        print("4. View Delivery Fee Report")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            display_packages(packages)
        elif choice == "2":
            assign_driver(packages)
        elif choice == "3":
            mark_delivered(packages)
        elif choice == "4":
            display_fee_report(packages)
        elif choice == "5":
            display_summary(packages)
            print("Thank you for using the Package Delivery Tracking System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.\n")


if __name__ == "__main__":
    main()