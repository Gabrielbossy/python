"""
Student Grade Management System
---------------------------------
A simple console-based program to manage student grades.
"""


def add_student(students):
    """Add a new student to the list, with an empty grades list."""
    name = input("Enter student name: ").strip()
    students.append({"name": name, "grades": []})
    print(f'"{name}" has been added.\n')


def calculate_average(grades):
    """Calculate and return the average of a list of grades."""
    if not grades:
        return 0
    return sum(grades) / len(grades)


def add_grade(students):
    """Add a grade to a specific student, after validating it's 0-100."""
    name = input("Enter the student's name: ").strip()

    # Find the student (case-insensitive match)
    student = None
    for s in students:
        if s["name"].lower() == name.lower():
            student = s
            break

    if student is None:
        print(f'No student named "{name}" was found.\n')
        return

    try:
        grade = float(input("Enter the grade (0-100): "))
    except ValueError:
        print("Invalid grade. Please enter a number.\n")
        return

    if grade < 0 or grade > 100:
        print("Grade must be between 0 and 100.\n")
        return

    student["grades"].append(grade)
    print(f"Grade {grade} added for {student['name']}.\n")


def display_students(students):
    """Display each student's name, grades, and average."""
    print("\n--- Students ---")
    if not students:
        print("No students have been added yet.")
    else:
        for s in students:
            avg = calculate_average(s["grades"])
            print(f"{s['name']}: grades={s['grades']}, average={avg:.2f}")
    print("----------------\n")


def display_top_student(students):
    """Find and display the student with the highest average grade."""
    students_with_grades = [s for s in students if s["grades"]]

    if not students_with_grades:
        print("No grades have been entered yet.\n")
        return

    top_student = max(
        students_with_grades,
        key=lambda s: calculate_average(s["grades"])
    )
    top_avg = calculate_average(top_student["grades"])
    print(f"\nTop student: {top_student['name']} with an average of {top_avg:.2f}\n")


def display_summary(students):
    """Display the final summary before exiting."""
    total_students = len(students)
    all_grades = []
    for s in students:
        all_grades.extend(s["grades"])

    total_grades = len(all_grades)
    class_average = calculate_average(all_grades)

    print("\n=== Final Summary ===")
    print(f"Total number of students: {total_students}")
    print(f"Total number of grades entered: {total_grades}")
    print(f"Class-wide average: {class_average:.2f}")
    print("======================\n")


def main():
    students = []

    while True:
        try:
            num_students = int(input("Enter the number of students: "))
            if num_students <= 0:
                print("Please enter a positive number.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    print()
    for i in range(num_students):
        add_student(students)

    while True:
        print("Grade Management Menu")
        print("1. Add Grade to Student")
        print("2. View All Students and Averages")
        print("3. View Top Student")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            add_grade(students)
        elif choice == "2":
            display_students(students)
        elif choice == "3":
            display_top_student(students)
        elif choice == "4":
            display_summary(students)
            print("Thank you for using the Grade Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.\n")


if __name__ == "__main__":
    main()