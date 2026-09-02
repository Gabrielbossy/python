"""
Theater Seating Chart System
----------------------------------
A simple console-based program managing a seating chart as a 2D grid
(a list of lists), demonstrating nested loops.
"""


def create_seating_chart(rows, columns):
    """Build and return a 2D grid of 'O' (open) seats using a nested loop."""
    chart = []
    for row in range(rows):          # outer loop: builds each row
        current_row = []
        for column in range(columns):  # inner loop: fills that row with seats
            current_row.append("O")
        chart.append(current_row)
    return chart


def display_chart(chart):
    """Print the seating chart as a grid, using a nested loop."""
    print("\n--- Seating Chart ---")
    for row in chart:                # outer loop: one row at a time
        row_display = ""
        for seat in row:             # inner loop: one seat at a time
            row_display += seat + " "
        print(row_display.strip())
    print("(O = Open, X = Booked)")
    print("----------------------\n")


def book_seat(chart, row, column):
    """Book a specific seat, given 1-based row/column numbers from the user."""
    total_rows = len(chart)
    total_columns = len(chart[0]) if chart else 0

    if row < 1 or row > total_rows or column < 1 or column > total_columns:
        print(f"Invalid seat. Rows must be 1-{total_rows}, columns must be 1-{total_columns}.\n")
        return

    # Convert 1-based (human-friendly) numbering to 0-based (Python) indexing.
    row_index = row - 1
    column_index = column - 1

    if chart[row_index][column_index] == "X":
        print(f"Seat (Row {row}, Seat {column}) is already booked.\n")
        return

    chart[row_index][column_index] = "X"
    print(f"Seat (Row {row}, Seat {column}) booked successfully.\n")


def count_available_seats(chart):
    """Count and return how many seats are still 'O', using a nested loop."""
    count = 0
    for row in chart:           # outer loop: each row
        for seat in row:        # inner loop: each seat in that row
            if seat == "O":
                count += 1
    return count


def display_summary(chart):
    """Display the final summary before exiting."""
    total_rows = len(chart)
    total_columns = len(chart[0]) if chart else 0
    total_seats = total_rows * total_columns
    available = count_available_seats(chart)
    booked = total_seats - available

    print("\n=== Theater Summary ===")
    print(f"Total number of seats: {total_seats}")
    print(f"Seats still available: {available}")
    print(f"Seats booked: {booked}")
    print("========================\n")


def main():
    while True:
        try:
            rows = int(input("Enter the number of rows: "))
            columns = int(input("Enter the number of seats per row: "))
            if rows <= 0 or columns <= 0:
                print("Both rows and columns must be positive numbers.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter whole numbers.")

    chart = create_seating_chart(rows, columns)

    while True:
        print("Theater Menu")
        print("1. View Seating Chart")
        print("2. Book a Seat")
        print("3. View Available Seat Count")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            display_chart(chart)
        elif choice == "2":
            try:
                row = int(input("Enter row number: "))
                column = int(input("Enter seat number: "))
            except ValueError:
                print("Invalid row or seat number.\n")
                continue
            book_seat(chart, row, column)
        elif choice == "3":
            print(f"\nAvailable seats: {count_available_seats(chart)}\n")
        elif choice == "4":
            display_summary(chart)
            print("Thank you for using the Theater Seating Chart System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.\n")


if __name__ == "__main__":
    main()