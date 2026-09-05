# Task 28: User Account Registration & Validation System

## Problem Statement
A website wants a program to register user accounts, enforcing rules on usernames and password strength.

## Requirements

Create the following functions:
- `register_user(users)`
- `is_valid_username(username, users)`
- `check_password_strength(password)`
- `login(users)`
- `display_users(users)`

The program should:

- Ask for the number of users to register initially.
- Store each user as a dictionary with a username and password, e.g. `{"username": "kito92", "password": "Str0ngPass!"}`.
- Display a menu:
  ```
  1. Register New User
  2. Attempt Login
  3. View Registered Usernames
  4. Exit
  ```

`is_valid_username(username, users)` should check and return `True` only if:
- The username is at least 4 characters long, **and**
- The username contains only letters and digits (no spaces or symbols — hint: look into the string method `.isalnum()`), **and**
- The username is not already taken by an existing user (case-insensitive check).

If any rule fails, it should return `False` (you don't need to say *which* rule failed inside this function — just `True`/`False`; the calling code can decide what message to show).

`check_password_strength(password)` should check the password against these rules and return a list of any rules that were **violated** (an empty list means the password is strong):
- Must be at least 8 characters long
- Must contain at least one uppercase letter (hint: loop through the characters and use `.isupper()`, or check `password.lower() != password`)
- Must contain at least one digit (hint: `.isdigit()` on each character)
- Must contain at least one of these symbols: `!@#$%^&*`

If a user registers:
- Ask for a username.
- Validate it with `is_valid_username`. If invalid, explain why (you can re-check the individual rules here to give a helpful message) and don't register the user.
- Ask for a password.
- Check it with `check_password_strength`. If any rules are violated, list them and don't register the user.
- If both checks pass, add the user to `users`.

If a user attempts to log in:
- Ask for a username and password.
- Check if a user with that username and password combination exists (case-insensitive username, case-sensitive password).
- Display success or failure accordingly.

Before exiting, display:
- Total number of registered users
- Number of successful login attempts made during this session
- Number of failed login attempts made during this session

## Concepts Tested
- String methods (`.isalnum()`, `.isupper()`, `.isdigit()`, `.lower()`)
- String iteration (looping through characters)
- Functions returning lists/booleans
- Conditional statements
- Loops
- Variables
- User input