"""
Employee Payroll System
--------------------------
A simple console-based program to manage employee hours and pay.
"""


def add_employee(employees):
    """Add a new employee with a name and hourly rate."""
    name = input("Enter employee name: ").strip()
    try:
        hourly_rate = float(input(f"Enter hourly rate for {name}: "))
        if hourly_rate < 0:
            print("Hourly rate cannot be negative.\n")
            return
    except ValueError:
        print("Invalid hourly rate. Please enter a number.\n")
        return

    employees.append({"name": name, "hourly_rate": hourly_rate, "hours_worked": 0})
    print(f'"{name}" added at ${hourly_rate:.2f}/hour.\n')


def calculate_pay(hours_worked, hourly_rate):
    """Calculate and return total pay for hours worked at a given rate."""
    return hours_worked * hourly_rate


def log_hours(employees):
    """Log hours worked for a specific employee."""
    name = input("Enter the employee's name: ").strip()

    employee = None
    for e in employees:
        if e["name"].lower() == name.lower():
            employee = e
            break

    if employee is None:
        print(f'No employee named "{name}" was found.\n')
        return

    try:
        hours = float(input("Enter hours worked: "))
        if hours <= 0:
            print("Hours must be a positive number.\n")
            return
    except ValueError:
        print("Invalid number of hours.\n")
        return

    employee["hours_worked"] += hours
    print(f"Logged {hours} hours for {employee['name']}.\n")


def display_employees(employees):
    """Display each employee's name, rate, hours, and total pay."""
    print("\n--- Employees ---")
    if not employees:
        print("No employees have been added yet.")
    else:
        for e in employees:
            pay = calculate_pay(e["hours_worked"], e["hourly_rate"])
            print(
                f"{e['name']}: rate=${e['hourly_rate']:.2f}/hr, "
                f"hours={e['hours_worked']}, pay=${pay:.2f}"
            )
    print("-----------------\n")


def display_highest_paid(employees):
    """Find and display the employee with the highest total pay."""
    employees_with_hours = [e for e in employees if e["hours_worked"] > 0]

    if not employees_with_hours:
        print("No hours have been logged yet.\n")
        return

    top_employee = max(
        employees_with_hours,
        key=lambda e: calculate_pay(e["hours_worked"], e["hourly_rate"])
    )
    top_pay = calculate_pay(top_employee["hours_worked"], top_employee["hourly_rate"])
    print(f"\nHighest paid: {top_employee['name']} with ${top_pay:.2f}\n")


def display_summary(employees):
    """Display the final payroll summary before exiting."""
    total_employees = len(employees)
    total_hours = sum(e["hours_worked"] for e in employees)
    total_payroll = sum(
        calculate_pay(e["hours_worked"], e["hourly_rate"]) for e in employees
    )

    print("\n=== Payroll Summary ===")
    print(f"Total number of employees: {total_employees}")
    print(f"Total hours logged: {total_hours}")
    print(f"Total payroll amount: ${total_payroll:.2f}")
    print("========================\n")


def main():
    employees = []

    while True:
        try:
            num_employees = int(input("Enter the number of employees: "))
            if num_employees <= 0:
                print("Please enter a positive number.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    print()
    for i in range(num_employees):
        add_employee(employees)

    while True:
        print("Payroll Menu")
        print("1. Log Hours for Employee")
        print("2. View All Employees & Pay")
        print("3. View Highest Paid Employee")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            log_hours(employees)
        elif choice == "2":
            display_employees(employees)
        elif choice == "3":
            display_highest_paid(employees)
        elif choice == "4":
            display_summary(employees)
            print("Thank you for using the Payroll System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.\n")


if __name__ == "__main__":
    main()