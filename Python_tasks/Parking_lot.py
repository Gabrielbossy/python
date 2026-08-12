"""
Parking Lot Management System
----------------------------------
A simple console-based program to manage vehicle check-ins and check-outs.
"""

HOURLY_RATE = 2


def display_spots(spots):
    """Display all currently available parking spots."""
    print("\n--- Available Spots ---")
    if not spots:
        print("No spots available. The parking lot is full!")
    else:
        print(spots)
    print("------------------------\n")


def calculate_fee(hours_parked, hourly_rate):
    """Calculate and return the parking fee for the given hours."""
    return hours_parked * hourly_rate


def check_in(spots, parked_vehicles):
    """Check in a vehicle, assigning it to an available spot."""
    if not spots:
        print("Sorry, the parking lot is full.\n")
        return

    display_spots(spots)
    plate = input("Enter the vehicle's license plate: ").strip().upper()

    try:
        spot_number = int(input("Enter the spot number to park in: "))
    except ValueError:
        print("Invalid spot number.\n")
        return

    if spot_number not in spots:
        print(f"Spot {spot_number} is not available.\n")
        return

    spots.remove(spot_number)
    parked_vehicles.append({"plate": plate, "spot": spot_number, "hours": 0})
    print(f"Vehicle {plate} checked in at spot {spot_number}.\n")


def find_vehicle(parked_vehicles, plate):
    """Helper function to find a parked vehicle by plate number."""
    for vehicle in parked_vehicles:
        if vehicle["plate"] == plate:
            return vehicle
    return None


def check_out(spots, parked_vehicles):
    """Check out a vehicle, calculate its fee, and free up its spot."""
    if not parked_vehicles:
        print("There are no vehicles currently parked.\n")
        return 0

    plate = input("Enter the license plate to check out: ").strip().upper()
    vehicle = find_vehicle(parked_vehicles, plate)

    if vehicle is None:
        print(f"No vehicle with plate {plate} is currently parked.\n")
        return 0

    try:
        hours = float(input("Enter the number of hours parked: "))
        if hours < 0:
            print("Hours cannot be negative.\n")
            return 0
    except ValueError:
        print("Invalid number of hours.\n")
        return 0

    fee = calculate_fee(hours, HOURLY_RATE)

    parked_vehicles.remove(vehicle)
    spots.append(vehicle["spot"])
    spots.sort()

    print(f"Vehicle {plate} checked out from spot {vehicle['spot']}.")
    print(f"Parking fee: ${fee:.2f}\n")
    return fee


def display_parked(parked_vehicles):
    """Display all currently parked vehicles."""
    print("\n--- Parked Vehicles ---")
    if not parked_vehicles:
        print("No vehicles are currently parked.")
    else:
        for vehicle in parked_vehicles:
            print(f"Plate: {vehicle['plate']} - Spot: {vehicle['spot']}")
    print("------------------------\n")


def display_summary(spots, total_spots, parked_vehicles, total_revenue):
    """Display the final summary before exiting."""
    print("\n=== Parking Summary ===")
    print(f"Total number of spots: {total_spots}")
    print(f"Spots currently available: {len(spots)}")
    print(f"Vehicles currently parked: {len(parked_vehicles)}")
    print(f"Total revenue collected: ${total_revenue:.2f}")
    print("========================\n")


def main():
    while True:
        try:
            num_spots = int(input("Enter the number of parking spots: "))
            if num_spots <= 0:
                print("Please enter a positive number.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    spots = list(range(1, num_spots + 1))
    total_spots = num_spots
    parked_vehicles = []
    total_revenue = 0

    while True:
        print("Parking Lot Menu")
        print("1. View Available Spots")
        print("2. Check In Vehicle")
        print("3. Check Out Vehicle")
        print("4. View Parked Vehicles")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            display_spots(spots)
        elif choice == "2":
            check_in(spots, parked_vehicles)
        elif choice == "3":
            total_revenue += check_out(spots, parked_vehicles)
        elif choice == "4":
            display_parked(parked_vehicles)
        elif choice == "5":
            display_summary(spots, total_spots, parked_vehicles, total_revenue)
            print("Thank you for using the Parking Lot Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.\n")


if __name__ == "__main__":
    main()