# Task 15: Pet Adoption Center Management System

## Problem Statement
An animal shelter wants a program to manage pets available for adoption and track adoptions.

## Requirements

Create the following functions:
- `add_pet(pets)`
- `adopt_pet(pets, adoptions)`
- `return_pet(pets, adoptions)`
- `calculate_fee(age, base_fee)`
- `display_pets(pets)`

The program should:

- Ask for the number of pets.
- Store each pet as a dictionary with a name, species, age (in years), and status, e.g. `{"name": "Rex", "species": "Dog", "age": 2, "status": "Available"}`.
- Display a menu:
  ```
  1. View All Pets
  2. Adopt a Pet
  3. Return a Pet
  4. View Adoption Records
  5. Exit
  ```

If someone adopts a pet:
- Show available pets (status is "Available").
- Ask for the pet's name.
- Check the pet exists and is available.
- Ask the adopter's name.
- Calculate the adoption fee (using `calculate_fee` — use a base fee of $50, but pets aged 5 or older get a reduced fee of half the base fee, to encourage adopting older pets).
- Mark the pet's status as "Adopted".
- Store the adoption as a dictionary with pet name, adopter name, and fee paid, and add it to `adoptions`.
- Display the fee charged.

If a pet is returned to the shelter:
- Ask for the pet's name.
- Check if it is currently marked "Adopted".
- Mark its status back to "Available".
- Remove the matching record from `adoptions`.

When viewing adoption records, show every adopter's name, the pet they adopted, and the fee paid.

Before exiting, display:
- Total number of pets
- Number of pets still available
- Number of pets adopted
- Total fees collected from all adoptions

## Concepts Tested
- Dictionaries
- Lists
- Functions
- Loops
- Conditional statements
- Variables
- User input
- List/dictionary manipulation