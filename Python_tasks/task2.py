#Library Book Management System

#Function to add books
def add_book(books):
    n = int(input("Enter the number of books: "))

    for i in range(n):
        title = input(f"Enter title of book {i + 1}: ")
        books.append(title)


# Function to display books
def display_books(books):
    if len(books) == 0:
        print("No books available.")
    else:
        print("\nAvailable Books:")
        for book in books:
            print(book)


# Function to borrow a book
def borrow_book(books):
    book = input("Enter the title of the book to borrow: ")

    if book in books:
        books.remove(book)
        print("Book borrowed successfully.")
        return 1
    else:
        print("Book not found.")
        return 0


# Function to return a book
def return_book(books):
    book = input("Enter the title of the book to return: ")
    books.append(book)
    print("Book returned successfully.")
    return 1


# Main Program

books = []

borrowed_count = 0
returned_count = 0

# Add books
add_book(books)

while True:

    print("\n===== LIBRARY MENU =====")
    print("1. View Books")
    print("2. Borrow Book")
    print("3. Return Book")
    print("4. Exit")

    choice = int(input("Enter your choice: "))

    if choice == 1:
        display_books(books)

    elif choice == 2:
        borrowed_count += borrow_book(books)

    elif choice == 3:
        returned_count += return_book(books)

    elif choice == 4:
        print("\n===== LIBRARY REPORT =====")
        print("Total books available:", len(books))
        print("Number of books borrowed:", borrowed_count)
        print("Number of books returned:", returned_count)

        print("\nFinal List of Books:")
        for book in books:
            print(book)

        print("Thank you!")
        break

    else:
        print("Invalid choice! Please enter 1, 2, 3 or 4.")