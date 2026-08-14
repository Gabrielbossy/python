"""
Course Enrollment System
-----------------------------
A simple console-based program to manage student enrollment into courses.
"""


def add_course(courses):
    """Add a new course with a name and capacity."""
    name = input("Enter course name: ").strip()

    try:
        capacity = int(input(f"Enter capacity for {name}: "))
        if capacity <= 0:
            print("Capacity must be a positive number.\n")
            return
    except ValueError:
        print("Invalid capacity. Please enter a whole number.\n")
        return

    courses.append({"name": name, "capacity": capacity, "students": []})
    print(f'Course "{name}" added with {capacity} seat(s).\n')


def find_course(courses, name):
    """Helper function to find a course by name (case-insensitive)."""
    for course in courses:
        if course["name"].lower() == name.lower():
            return course
    return None


def enroll_student(courses):
    """Enroll a student into a course, if there is space."""
    course_name = input("Enter the course name: ").strip()
    course = find_course(courses, course_name)

    if course is None:
        print(f'Course "{course_name}" was not found.\n')
        return

    if len(course["students"]) >= course["capacity"]:
        print(f'Course "{course["name"]}" is full.\n')
        return

    student_name = input("Enter the student's name: ").strip()

    if student_name.lower() in [s.lower() for s in course["students"]]:
        print(f'{student_name} is already enrolled in "{course["name"]}".\n')
        return

    course["students"].append(student_name)
    print(f'{student_name} enrolled in "{course["name"]}".\n')


def drop_student(courses):
    """Remove a student from a course."""
    course_name = input("Enter the course name: ").strip()
    course = find_course(courses, course_name)

    if course is None:
        print(f'Course "{course_name}" was not found.\n')
        return

    student_name = input("Enter the student's name: ").strip()

    for student in course["students"]:
        if student.lower() == student_name.lower():
            course["students"].remove(student)
            print(f'{student} has been dropped from "{course["name"]}".\n')
            return

    print(f'{student_name} is not enrolled in "{course["name"]}".\n')


def display_courses(courses):
    """Display all courses, their enrolled students, and seats remaining."""
    print("\n--- Courses ---")
    if not courses:
        print("No courses have been added yet.")
    else:
        for course in courses:
            seats_left = course["capacity"] - len(course["students"])
            students = ", ".join(course["students"]) if course["students"] else "None"
            print(
                f'{course["name"]} - Students: {students} - '
                f"Seats remaining: {seats_left}"
            )
    print("---------------\n")


def course_report(courses):
    """Display each course's fill status."""
    print("\n--- Course Report ---")
    if not courses:
        print("No courses have been added yet.")
    else:
        for course in courses:
            seats_left = course["capacity"] - len(course["students"])
            if seats_left == 0:
                print(f'{course["name"]}: FULL')
            else:
                print(f'{course["name"]}: {seats_left} seat(s) remaining')
    print("----------------------\n")


def display_summary(courses):
    """Display the final summary before exiting."""
    total_courses = len(courses)
    total_enrollments = sum(len(course["students"]) for course in courses)

    print("\n=== Enrollment Summary ===")
    print(f"Total number of courses: {total_courses}")
    print(f"Total enrollments across all courses: {total_enrollments}")

    if courses:
        most_popular = max(courses, key=lambda c: len(c["students"]))
        print(
            f'Most popular course: {most_popular["name"]} '
            f'({len(most_popular["students"])} student(s))'
        )
    else:
        print("Most popular course: N/A (no courses)")
    print("===========================\n")


def main():
    courses = []

    while True:
        try:
            num_courses = int(input("Enter the number of courses to set up: "))
            if num_courses <= 0:
                print("Please enter a positive number.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    print()
    for i in range(num_courses):
        print(f"Course {i + 1}:")
        add_course(courses)

    while True:
        print("Course Menu")
        print("1. View All Courses")
        print("2. Enroll Student")
        print("3. Drop Student")
        print("4. Course Report (Full/Available Seats)")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            display_courses(courses)
        elif choice == "2":
            enroll_student(courses)
        elif choice == "3":
            drop_student(courses)
        elif choice == "4":
            course_report(courses)
        elif choice == "5":
            display_summary(courses)
            print("Thank you for using the Course Enrollment System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.\n")


if __name__ == "__main__":
    main()