"""
Bank Account Management System
---------------------------------
A simple console-based program to manage customer bank accounts.
"""

STARTING_ACCOUNT_NUMBER = 1001


def create_account(accounts):
    """Create a new account with an auto-generated account number."""
    name = input("Enter account holder's name: ").strip()
    account_number = STARTING_ACCOUNT_NUMBER + len(accounts)

    accounts.append({"name": name, "account_number": account_number, "balance": 0})
    print(f'Account created for "{name}". Account number: {account_number}\n')


def find_account(accounts, account_number):
    """Helper function to find an account by its account number."""
    for account in accounts:
        if account["account_number"] == account_number:
            return account
    return None


def deposit(accounts):
    """Deposit money into an account."""
    try:
        account_number = int(input("Enter account number: "))
    except ValueError:
        print("Invalid account number.\n")
        return

    account = find_account(accounts, account_number)
    if account is None:
        print(f"No account found with number {account_number}.\n")
        return

    try:
        amount = float(input("Enter deposit amount: "))
        if amount <= 0:
            print("Deposit amount must be positive.\n")
            return
    except ValueError:
        print("Invalid amount.\n")
        return

    account["balance"] += amount
    print(f"Deposited ${amount:.2f}. New balance: ${account['balance']:.2f}\n")


def withdraw(accounts):
    """Withdraw money from an account."""
    try:
        account_number = int(input("Enter account number: "))
    except ValueError:
        print("Invalid account number.\n")
        return

    account = find_account(accounts, account_number)
    if account is None:
        print(f"No account found with number {account_number}.\n")
        return

    try:
        amount = float(input("Enter withdrawal amount: "))
        if amount <= 0:
            print("Withdrawal amount must be positive.\n")
            return
    except ValueError:
        print("Invalid amount.\n")
        return

    if amount > account["balance"]:
        print(f"Insufficient funds. Current balance: ${account['balance']:.2f}\n")
        return

    account["balance"] -= amount
    print(f"Withdrew ${amount:.2f}. New balance: ${account['balance']:.2f}\n")


def check_balance(accounts):
    """Display the balance of a specific account."""
    try:
        account_number = int(input("Enter account number: "))
    except ValueError:
        print("Invalid account number.\n")
        return

    account = find_account(accounts, account_number)
    if account is None:
        print(f"No account found with number {account_number}.\n")
        return

    print(f"Account {account_number} ({account['name']}) balance: ${account['balance']:.2f}\n")


def display_accounts(accounts):
    """Display all accounts and their balances."""
    print("\n--- Accounts ---")
    if not accounts:
        print("No accounts have been created yet.")
    else:
        for account in accounts:
            print(
                f"#{account['account_number']} - {account['name']}: "
                f"${account['balance']:.2f}"
            )
    print("----------------\n")


def display_summary(accounts):
    """Display the final summary before exiting."""
    total_accounts = len(accounts)
    total_money = sum(account["balance"] for account in accounts)

    print("\n=== Bank Summary ===")
    print(f"Total number of accounts: {total_accounts}")
    print(f"Total money held across all accounts: ${total_money:.2f}")

    if accounts:
        richest = max(accounts, key=lambda a: a["balance"])
        print(
            f"Highest balance: {richest['name']} (Account #{richest['account_number']}) "
            f"with ${richest['balance']:.2f}"
        )
    else:
        print("Highest balance: N/A (no accounts)")
    print("=====================\n")


def main():
    accounts = []

    while True:
        try:
            num_accounts = int(input("Enter the number of accounts to create: "))
            if num_accounts <= 0:
                print("Please enter a positive number.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    print()
    for i in range(num_accounts):
        create_account(accounts)

    while True:
        print("Bank Menu")
        print("1. View All Accounts")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Check Balance")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            display_accounts(accounts)
        elif choice == "2":
            deposit(accounts)
        elif choice == "3":
            withdraw(accounts)
        elif choice == "4":
            check_balance(accounts)
        elif choice == "5":
            display_summary(accounts)
            print("Thank you for banking with us. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.\n")


if __name__ == "__main__":
    main()