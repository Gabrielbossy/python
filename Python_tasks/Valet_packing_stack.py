"""
Valet Parking Stack System
--------------------------------
A simple console-based program modeling a single-lane valet driveway,
where only the last car parked can be retrieved (a stack / LIFO structure).
"""


def park_car(lane, parked_cars):
    """Park a car at the top of the lane (the end of the list)."""
    plate = input("Enter license plate: ").strip().upper()
    owner = input("Enter owner's name: ").strip()

    car = {"plate": plate, "owner": owner}

    # Adding to the END of the list -> this becomes the "top" of the stack.
    lane.append(car)
    parked_cars.append(car)  # permanent history, never removed

    print(f"Car {plate} ({owner}) parked at the top of the lane.\n")


def retrieve_last_car(lane):
    """Retrieve the car at the TOP of the lane (last one parked)."""
    if not lane:
        print("The lane is empty. No cars to retrieve.\n")
        return

    # Removing from the END of the list -> this is the LIFO rule.
    # Note: lane.pop() with no argument removes the LAST item by default.
    # If we wanted a queue instead (first car in, first out), we'd use
    # lane.pop(0) to remove from the FRONT instead - that's the key
    # difference between a stack and a queue.
    car = lane.pop()

    print(f"Retrieved Car {car['plate']} ({car['owner']}) from the top of the lane.\n")


def view_lane(lane):
    """Display every car currently in the lane, top of stack first."""
    print("\n--- Current Lane (top to bottom) ---")
    if not lane:
        print("The lane is empty.")
    else:
        # reversed() lets us print from the END of the list first,
        # since the end of the list represents the "top" of the stack.
        for position, car in enumerate(reversed(lane), start=1):
            print(f"{position}. {car['plate']} - {car['owner']}")
    print("-------------------------------------\n")


def total_cars_parked(parked_cars):
    """Calculate and return the total number of cars ever parked."""
    return len(parked_cars)


def view_history(parked_cars):
    """Display every car that has ever been parked."""
    print("\n--- Parking History ---")
    if not parked_cars:
        print("No cars have been parked yet.")
    else:
        for car in parked_cars:
            print(f"{car['plate']} - {car['owner']}")
    print("------------------------\n")


def display_summary(lane, parked_cars):
    """Display the final summary before exiting."""
    total_ever_parked = total_cars_parked(parked_cars)
    currently_in_lane = len(lane)
    retrieved_count = total_ever_parked - currently_in_lane

    print("\n=== Valet Summary ===")
    print(f"Total cars ever parked: {total_ever_parked}")
    print(f"Cars currently in the lane: {currently_in_lane}")
    print(f"Cars retrieved so far: {retrieved_count}")

    if lane:
        top_car = lane[-1]  # the last item in the list is the top of the stack
        print(f"Car at the top of the lane: {top_car['plate']} ({top_car['owner']})")
    else:
        print("Car at the top of the lane: None (lane is empty)")
    print("======================\n")


def main():
    lane = []
    parked_cars = []

    while True:
        print("Valet Parking Menu")
        print("1. Park a Car")
        print("2. Retrieve Last Parked Car")
        print("3. View Lane")
        print("4. View Parking History")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            park_car(lane, parked_cars)
        elif choice == "2":
            retrieve_last_car(lane)
        elif choice == "3":
            view_lane(lane)
        elif choice == "4":
            view_history(parked_cars)
        elif choice == "5":
            display_summary(lane, parked_cars)
            print("Thank you for using the Valet Parking System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.\n")


if __name__ == "__main__":
    main()