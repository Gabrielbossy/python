def check_strength(password):
    feedback = []
    score = 0

    common_weak_passwords = ["password", "password123", "123456", "qwerty", "letmein", "admin"]

    if password.lower() in common_weak_passwords:
        return 0, ["This is a commonly used password. Choose something more unique."]

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Make it at least 8 characters long.")

    if any(char.isupper() for char in password):
        score += 1
    else:
        feedback.append("Add at least one uppercase letter.")

    if any(char.islower() for char in password):
        score += 1
    else:
        feedback.append("Add at least one lowercase letter.")

    if any(char.isdigit() for char in password):
        score += 1
    else:
        feedback.append("Add at least one number.")

    special_characters = "!@#$%^&*()-_=+[]{};:,.<>?/"
    if any(char in special_characters for char in password):
        score += 1
    else:
        feedback.append("Add at least one special character (e.g. !, @, #, $).")

    return score, feedback


def rate_strength(score):
    if score <= 1:
        return "Very Weak"
    elif score == 2:
        return "Weak"
    elif score == 3:
        return "Moderate"
    elif score == 4:
        return "Strong"
    else:
        return "Very Strong"


def main():
    password = input("Enter a password to check: ")
    score, feedback = check_strength(password)
    rating = rate_strength(score)

    print(f"\nStrength: {rating} ({score}/5)")

    if feedback:
        print("Suggestions to improve:")
        for tip in feedback:
            print(f"- {tip}")
    else:
        print("Great password! It meets all the criteria.")


if __name__ == "__main__":
    main()