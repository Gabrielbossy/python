"""
User Account Registration & Validation System
----------------------------------------------------
A simple console-based program to register users and validate
usernames/passwords, demonstrating string methods and iteration.
"""

MIN_USERNAME_LENGTH = 4
MIN_PASSWORD_LENGTH = 8
SPECIAL_SYMBOLS = "!@#$%^&*"


def is_valid_username(username, users):
    """Return True only if the username meets all rules."""
    if len(username) < MIN_USERNAME_LENGTH:
        return False

    # .isalnum() returns True only if EVERY character is a letter or digit
    # (no spaces, no symbols, no punctuation).
    if not username.isalnum():
        return False

    # Check it isn't already taken (case-insensitive).
    for user in users:
        if user["username"].lower() == username.lower():
            return False

    return True


def check_password_strength(password):
    """Return a list of rule violations. An empty list means it's strong."""
    violations = []

    if len(password) < MIN_PASSWORD_LENGTH:
        violations.append(f"Must be at least {MIN_PASSWORD_LENGTH} characters long")

    # Loop through each character checking for at least one uppercase letter.
    has_uppercase = False
    for character in password:
        if character.isupper():
            has_uppercase = True
            break
    if not has_uppercase:
        violations.append("Must contain at least one uppercase letter")

    # Same idea, but checking for at least one digit.
    has_digit = False
    for character in password:
        if character.isdigit():
            has_digit = True
            break
    if not has_digit:
        violations.append("Must contain at least one digit")

    # Same idea again, but checking for at least one special symbol.
    has_symbol = False
    for character in password:
        if character in SPECIAL_SYMBOLS:
            has_symbol = True
            break
    if not has_symbol:
        violations.append(f"Must contain at least one symbol ({SPECIAL_SYMBOLS})")

    return violations


def register_user(users):
    """Register a new user after validating username and password."""
    username = input("Choose a username: ").strip()

    if not is_valid_username(username, users):
        # Re-check individual rules here just to give a helpful message.
        if len(username) < MIN_USERNAME_LENGTH:
            print(f"Username must be at least {MIN_USERNAME_LENGTH} characters long.\n")
        elif not username.isalnum():
            print("Username can only contain letters and numbers (no symbols or spaces).\n")
        else:
            print(f'Username "{username}" is already taken.\n')
        return

    password = input("Choose a password: ").strip()
    violations = check_password_strength(password)

    if violations:
        print("Password does not meet the requirements:")
        for issue in violations:
            print(f"  - {issue}")
        print()
        return

    users.append({"username": username, "password": password})
    print(f'User "{username}" registered successfully.\n')


def login(users):
    """Attempt to log in with a username/password combination. Returns True/False."""
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    for user in users:
        if user["username"].lower() == username.lower() and user["password"] == password:
            print(f"Login successful. Welcome, {user['username']}!\n")
            return True

    print("Login failed. Incorrect username or password.\n")
    return False


def display_users(users):
    """Display all registered usernames (never display passwords)."""
    print("\n--- Registered Usernames ---")
    if not users:
        print("No users registered yet.")
    else:
        for user in users:
            print(user["username"])
    print("-----------------------------\n")


def display_summary(users, successful_logins, failed_logins):
    """Display the final summary before exiting."""
    print("\n=== Account System Summary ===")
    print(f"Total registered users: {len(users)}")
    print(f"Successful login attempts: {successful_logins}")
    print(f"Failed login attempts: {failed_logins}")
    print("===============================\n")


def main():
    users = []
    successful_logins = 0
    failed_logins = 0

    while True:
        try:
            num_users = int(input("Enter the number of users to register initially: "))
            if num_users < 0:
                print("Please enter a non-negative number.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    print()
    for i in range(num_users):
        print(f"User {i + 1}:")
        register_user(users)

    while True:
        print("Account Menu")
        print("1. Register New User")
        print("2. Attempt Login")
        print("3. View Registered Usernames")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            register_user(users)
        elif choice == "2":
            success = login(users)
            if success:
                successful_logins += 1
            else:
                failed_logins += 1
        elif choice == "3":
            display_users(users)
        elif choice == "4":
            display_summary(users, successful_logins, failed_logins)
            print("Thank you for using the Account Registration System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.\n")


if __name__ == "__main__":
    main()