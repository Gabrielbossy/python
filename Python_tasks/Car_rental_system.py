"""
Car Rental System
----------------------
A simple console-based program to manage a fleet of rental cars.
"""

CATEGORY_RATES = {
    "economy": 30,
    "sedan": 45,
    "suv": 70,
}


def add_car(cars):
    """Add a new car to the fleet."""
    plate = input("Enter the car's plate number: ").strip().upper()

    print(f"Available categories: {', '.join(c.title() for c in CATEGORY_RATES)}")
    category = input("Enter the car's category: ").strip().lower()

    if category not in CATEGORY_RATES:
        print(f'"{category}" is not a valid category. Car not added.\n')
        return

    cars.append({"plate": plate, "category": category.title(), "available": True})
    print(f"Car {plate} ({category.title()}) added to the fleet.\n")


def find_car(cars, plate):
    """Helper function to find a car by plate number."""
    for car in cars:
        if car["plate"] == plate:
            return car
    return None


def calculate_cost(days, daily_rate):
    """Calculate and return the total rental cost."""
    return days * daily_rate


def display_cars(cars):
    """Display all cars in the fleet and their availability."""
    print("\n--- Fleet ---")
    if not cars:
        print("No cars in the fleet.")
    else:
        for car in cars:
            status = "Available" if car["available"] else "Rented"
            print(f"{car['plate']} - {car['category']} - {status}")
    print("-------------\n")


def rent_car(cars, rentals):
    """Rent out a car if it exists and is available. Returns the cost charged."""
    available_cars = [c for c in cars if c["available"]]

    if not available_cars:
        print("No cars are currently available.\n")
        return 0

    print("\n--- Available Cars ---")
    for car in available_cars:
        print(f"{car['plate']} - {car['category']}")
    print("-----------------------\n")

    plate = input("Enter the plate number to rent: ").strip().upper()
    car = find_car(cars, plate)

    if car is None:
        print(f"No car found with plate {plate}.\n")
        return 0

    if not car["available"]:
        print(f"Car {plate} is not available.\n")
        return 0

    customer_name = input("Enter customer name: ").strip()

    try:
        days = int(input("Enter number of days: "))
        if days <= 0:
            print("Days must be a positive number.\n")
            return 0
    except ValueError:
        print("Invalid number of days.\n")
        return 0

    daily_rate = CATEGORY_RATES[car["category"].lower()]
    cost = calculate_cost(days, daily_rate)

    car["available"] = False
    rentals.append({"plate": plate, "customer": customer_name, "days": days})

    print(f"Car {plate} rented to {customer_name} for {days} day(s).")
    print(f"Total cost: ${cost}\n")
    return cost


def return_car(cars, rentals):
    """Return a rented car and remove it from active rentals."""
    plate = input("Enter the plate number to return: ").strip().upper()
    car = find_car(cars, plate)

    if car is None:
        print(f"No car found with plate {plate}.\n")
        return

    if car["available"]:
        print(f"Car {plate} is not currently rented.\n")
        return

    car["available"] = True

    for rental in rentals:
        if rental["plate"] == plate:
            rentals.remove(rental)
            break

    print(f"Car {plate} has been returned.\n")


def display_rentals(rentals):
    """Display all active rentals."""
    print("\n--- Active Rentals ---")
    if not rentals:
        print("No cars are currently rented out.")
    else:
        for rental in rentals:
            print(
                f"{rental['plate']} - {rental['customer']} - "
                f"{rental['days']} day(s)"
            )
    print("-----------------------\n")


def display_summary(cars, total_revenue):
    """Display the final summary before exiting."""
    total_cars = len(cars)
    available_count = sum(1 for car in cars if car["available"])
    rented_count = total_cars - available_count

    print("\n=== Rental Summary ===")
    print(f"Total number of cars: {total_cars}")
    print(f"Cars currently available: {available_count}")
    print(f"Cars currently rented out: {rented_count}")
    print(f"Total revenue generated: ${total_revenue}")
    print("=======================\n")


def main():
    cars = []
    rentals = []
    total_revenue = 0

    while True:
        try:
            num_cars = int(input("Enter the number of cars in the fleet: "))
            if num_cars <= 0:
                print("Please enter a positive number.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    print()
    for i in range(num_cars):
        print(f"Car {i + 1}:")
        add_car(cars)

    while True:
        print("Car Rental Menu")
        print("1. View All Cars")
        print("2. Rent a Car")
        print("3. Return a Car")
        print("4. View Active Rentals")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            display_cars(cars)
        elif choice == "2":
            total_revenue += rent_car(cars, rentals)
        elif choice == "3":
            return_car(cars, rentals)
        elif choice == "4":
            display_rentals(rentals)
        elif choice == "5":
            display_summary(cars, total_revenue)
            print("Thank you for using the Car Rental System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.\n")


if __name__ == "__main__":
    main()