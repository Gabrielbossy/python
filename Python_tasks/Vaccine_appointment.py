"""
Vaccine Appointment Scheduling System
----------------------------------------------
A simple console-based program to manage vaccine appointment slots.
"""


def add_slot(slots):
    """Add a new appointment slot with a time and capacity."""
    time = input("Enter slot time (e.g. 9:00 AM): ").strip()

    try:
        capacity = int(input(f"Enter capacity for the {time} slot: "))
        if capacity <= 0:
            print("Capacity must be a positive number.\n")
            return
    except ValueError:
        print("Invalid capacity. Please enter a whole number.\n")
        return

    slot_id = len(slots) + 1
    slots.append({"slot_id": slot_id, "time": time, "capacity": capacity, "booked": 0})
    print(f"Slot {slot_id} ({time}) added with capacity {capacity}.\n")


def find_slot(slots, slot_id):
    """Helper function to find a slot by its ID."""
    for slot in slots:
        if slot["slot_id"] == slot_id:
            return slot
    return None


def display_slots(slots):
    """Display all slots and their booking status."""
    print("\n--- Slots ---")
    if not slots:
        print("No slots have been created yet.")
    else:
        for slot in slots:
            print(
                f"Slot {slot['slot_id']} - {slot['time']} - "
                f"{slot['booked']}/{slot['capacity']} booked"
            )
    print("-------------\n")


def calculate_doses_given(appointments):
    """Calculate and return the number of doses given (active appointments)."""
    return len(appointments)


def book_appointment(slots, appointments):
    """Book a patient into a slot that still has space."""
    available_slots = [s for s in slots if s["booked"] < s["capacity"]]

    if not available_slots:
        print("No slots have space available.\n")
        return

    print("\n--- Available Slots ---")
    for slot in available_slots:
        print(
            f"Slot {slot['slot_id']} - {slot['time']} - "
            f"{slot['booked']}/{slot['capacity']} booked"
        )
    print("------------------------\n")

    try:
        slot_id = int(input("Enter the slot ID to book: "))
    except ValueError:
        print("Invalid slot ID.\n")
        return

    slot = find_slot(slots, slot_id)

    if slot is None:
        print(f"No slot found with ID {slot_id}.\n")
        return

    if slot["booked"] >= slot["capacity"]:
        print(f"Slot {slot_id} is full.\n")
        return

    patient_name = input("Enter patient's name: ").strip()

    slot["booked"] += 1
    appointments.append({"slot_id": slot_id, "patient": patient_name, "time": slot["time"]})

    print(f"Appointment booked for {patient_name} at {slot['time']} (Slot {slot_id}).\n")


def cancel_appointment(slots, appointments):
    """Cancel a patient's appointment and free up space in their slot."""
    patient_name = input("Enter the patient's name: ").strip()

    matching_appointment = None
    for appointment in appointments:
        if appointment["patient"].lower() == patient_name.lower():
            matching_appointment = appointment
            break

    if matching_appointment is None:
        print(f'No appointment found for "{patient_name}".\n')
        return

    slot = find_slot(slots, matching_appointment["slot_id"])
    if slot is not None:
        slot["booked"] -= 1

    appointments.remove(matching_appointment)
    print(f"Appointment for {patient_name} has been cancelled.\n")


def display_appointments(appointments):
    """Display all booked appointments."""
    print("\n--- Appointment Records ---")
    if not appointments:
        print("No appointments have been booked yet.")
    else:
        for appointment in appointments:
            print(
                f"{appointment['patient']} - Slot {appointment['slot_id']} - "
                f"{appointment['time']}"
            )
    print("----------------------------\n")


def display_summary(slots, appointments):
    """Display the final summary before exiting."""
    total_slots = len(slots)
    total_capacity = sum(slot["capacity"] for slot in slots)
    doses_given = calculate_doses_given(appointments)

    print("\n=== Clinic Summary ===")
    print(f"Total number of slots: {total_slots}")
    print(f"Total appointment capacity: {total_capacity}")
    print(f"Doses given: {doses_given}")

    if slots:
        busiest_slot = max(slots, key=lambda s: s["booked"])
        print(
            f"Busiest slot: Slot {busiest_slot['slot_id']} ({busiest_slot['time']}) "
            f"with {busiest_slot['booked']} booking(s)"
        )
    else:
        print("Busiest slot: N/A (no slots)")
    print("=======================\n")


def main():
    slots = []
    appointments = []

    while True:
        try:
            num_slots = int(input("Enter the number of time slots to create: "))
            if num_slots <= 0:
                print("Please enter a positive number.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    print()
    for i in range(num_slots):
        print(f"Slot {i + 1}:")
        add_slot(slots)

    while True:
        print("Vaccine Appointment Menu")
        print("1. View All Slots")
        print("2. Book Appointment")
        print("3. Cancel Appointment")
        print("4. View Appointment Records")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            display_slots(slots)
        elif choice == "2":
            book_appointment(slots, appointments)
        elif choice == "3":
            cancel_appointment(slots, appointments)
        elif choice == "4":
            display_appointments(appointments)
        elif choice == "5":
            display_summary(slots, appointments)
            print("Thank you for using the Vaccine Appointment System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.\n")


if __name__ == "__main__":
    main()