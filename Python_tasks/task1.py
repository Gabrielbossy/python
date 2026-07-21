
"""
Hotel Room Booking System
--------------------------
A simple console-based program to manage hotel room bookings.
"""

ROOM_PRICE = 100  # price per room per day (you can change this)


def show_rooms(available_rooms):
    """Display all currently available rooms."""
    print("\n--- Available Rooms ---")
    if not available_rooms:
        print("No rooms are currently available.")
    else:
        print(available_rooms)
    print("------------------------\n")


def calculate_bill(days, room_price):
    """Calculate and return the total bill for a stay."""
    return days * room_price


def book_room(available_rooms, booked_rooms):
    """Book a room if it exists in the available rooms list."""
    if not available_rooms:
        print("Sorry, no rooms are available at the moment.\n")
        return 0

    show_rooms(available_rooms)

    try:
        room_number = int(input("Enter the room number to book: "))
    except ValueError:
        print("Invalid room number.\n")
        return 0

    if room_number not in available_rooms:
        print(f"Room {room_number} is not available.\n")
        return 0

    try:
        days = int(input("Enter the number of days you will stay: "))
        if days <= 0:
            print("Number of days must be positive.\n")
            return 0
    except ValueError:
        print("Invalid number of days.\n")
        return 0

    available_rooms.remove(room_number)
    booked_rooms.append(room_number)

    bill = calculate_bill(days, ROOM_PRICE)
    print(f"Room {room_number} booked successfully for {days} day(s).")
    print(f"Total bill: {bill}\n")

    return bill


def cancel_booking(available_rooms, booked_rooms):
    """Cancel a booking and return the room to the available list."""
    if not booked_rooms:
        print("There are no booked rooms to cancel.\n")
        return

    print(f"Currently booked rooms: {booked_rooms}")

    try:
        room_number = int(input("Enter the room number to cancel: "))
    except ValueError:
        print("Invalid room number.\n")
        return

    if room_number not in booked_rooms:
        print(f"Room {room_number} is not currently booked.\n")
        return

    booked_rooms.remove(room_number)
    available_rooms.append(room_number)
    available_rooms.sort()
    print(f"Booking for Room {room_number} has been cancelled.\n")


def display_summary(customer_name, available_rooms, booked_rooms, total_revenue):
    """Display the final summary before exiting."""
    print("\n=== Hotel Booking Summary ===")
    print(f"Customer name: {customer_name}")
    print(f"Rooms currently available: {available_rooms}")
    print(f"Rooms booked: {booked_rooms}")
    print(f"Total revenue generated: {total_revenue}")
    print("==============================\n")


def main():
    customer_name = input("Enter customer name: ").strip()

    while True:
        try:
            num_rooms = int(input("Enter the number of available rooms: "))
            if num_rooms <= 0:
                print("Please enter a positive number.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    # Create a list of room numbers, e.g. [101, 102, 103, 104, 105]
    starting_room_number = 101
    available_rooms = [starting_room_number + i for i in range(num_rooms)]
    booked_rooms = []
    total_revenue = 0

    while True:
        print("Hotel Menu")
        print("1. View Available Rooms")
        print("2. Book Room")
        print("3. Cancel Booking")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            show_rooms(available_rooms)
        elif choice == "2":
            total_revenue += book_room(available_rooms, booked_rooms)
        elif choice == "3":
            cancel_booking(available_rooms, booked_rooms)
        elif choice == "4":
            display_summary(customer_name, available_rooms, booked_rooms, total_revenue)
            print("Thank you for using the Hotel Room Booking System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.\n")


if __name__ == "__main__":
    main()