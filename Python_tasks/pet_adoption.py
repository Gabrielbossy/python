"""
Pet Adoption Center Management System
------------------------------------------
A simple console-based program to manage shelter pets and adoptions.
"""

BASE_FEE = 50
SENIOR_AGE_THRESHOLD = 5


def add_pet(pets):
    """Add a new pet to the shelter."""
    name = input("Enter pet name: ").strip()
    species = input("Enter species (e.g. Dog, Cat): ").strip()

    try:
        age = int(input(f"Enter {name}'s age (in years): "))
        if age < 0:
            print("Age cannot be negative.\n")
            return
    except ValueError:
        print("Invalid age. Please enter a whole number.\n")
        return

    pets.append({"name": name, "species": species, "age": age, "status": "Available"})
    print(f'"{name}" the {species} added, age {age}.\n')


def find_pet(pets, name):
    """Helper function to find a pet by name (case-insensitive)."""
    for pet in pets:
        if pet["name"].lower() == name.lower():
            return pet
    return None


def calculate_fee(age, base_fee):
    """Calculate and return the adoption fee, halved for senior pets."""
    if age >= SENIOR_AGE_THRESHOLD:
        return base_fee / 2
    return base_fee


def display_pets(pets):
    """Display all pets and their current status."""
    print("\n--- Pets ---")
    if not pets:
        print("No pets in the shelter.")
    else:
        for pet in pets:
            print(
                f"{pet['name']} - {pet['species']} - Age {pet['age']} - "
                f"{pet['status']}"
            )
    print("------------\n")


def adopt_pet(pets, adoptions):
    """Adopt out a pet if it exists and is available. Returns fee charged."""
    available_pets = [p for p in pets if p["status"] == "Available"]

    if not available_pets:
        print("No pets are currently available for adoption.\n")
        return 0

    print("\n--- Available Pets ---")
    for pet in available_pets:
        print(f"{pet['name']} - {pet['species']} - Age {pet['age']}")
    print("-----------------------\n")

    pet_name = input("Enter the name of the pet to adopt: ").strip()
    pet = find_pet(pets, pet_name)

    if pet is None:
        print(f'No pet named "{pet_name}" was found.\n')
        return 0

    if pet["status"] != "Available":
        print(f'"{pet["name"]}" is not available for adoption.\n')
        return 0

    adopter_name = input("Enter adopter's name: ").strip()
    fee = calculate_fee(pet["age"], BASE_FEE)

    pet["status"] = "Adopted"
    adoptions.append({"pet": pet["name"], "adopter": adopter_name, "fee": fee})

    print(f'{adopter_name} adopted "{pet["name"]}"! Fee charged: ${fee:.2f}\n')
    return fee


def return_pet(pets, adoptions):
    """Return an adopted pet back to the shelter."""
    pet_name = input("Enter the name of the pet being returned: ").strip()
    pet = find_pet(pets, pet_name)

    if pet is None:
        print(f'No pet named "{pet_name}" was found.\n')
        return

    if pet["status"] != "Adopted":
        print(f'"{pet["name"]}" is not currently marked as adopted.\n')
        return

    pet["status"] = "Available"

    for adoption in adoptions:
        if adoption["pet"].lower() == pet_name.lower():
            adoptions.remove(adoption)
            break

    print(f'"{pet["name"]}" has been returned to the shelter.\n')


def display_adoptions(adoptions):
    """Display all adoption records."""
    print("\n--- Adoption Records ---")
    if not adoptions:
        print("No adoptions have been made yet.")
    else:
        for adoption in adoptions:
            print(
                f"{adoption['adopter']} adopted {adoption['pet']} - "
                f"Fee: ${adoption['fee']:.2f}"
            )
    print("-------------------------\n")


def display_summary(pets, adoptions):
    """Display the final summary before exiting."""
    total_pets = len(pets)
    available_count = sum(1 for p in pets if p["status"] == "Available")
    adopted_count = total_pets - available_count
    total_fees = sum(a["fee"] for a in adoptions)

    print("\n=== Shelter Summary ===")
    print(f"Total number of pets: {total_pets}")
    print(f"Pets still available: {available_count}")
    print(f"Pets adopted: {adopted_count}")
    print(f"Total fees collected: ${total_fees:.2f}")
    print("========================\n")


def main():
    pets = []
    adoptions = []

    while True:
        try:
            num_pets = int(input("Enter the number of pets: "))
            if num_pets <= 0:
                print("Please enter a positive number.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    print()
    for i in range(num_pets):
        print(f"Pet {i + 1}:")
        add_pet(pets)

    while True:
        print("Pet Adoption Menu")
        print("1. View All Pets")
        print("2. Adopt a Pet")
        print("3. Return a Pet")
        print("4. View Adoption Records")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            display_pets(pets)
        elif choice == "2":
            adopt_pet(pets, adoptions)
        elif choice == "3":
            return_pet(pets, adoptions)
        elif choice == "4":
            display_adoptions(adoptions)
        elif choice == "5":
            display_summary(pets, adoptions)
            print("Thank you for using the Pet Adoption Center System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.\n")


if __name__ == "__main__":
    main()