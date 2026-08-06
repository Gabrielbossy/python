# Task 7: Bank Account Management System

## Problem Statement
A bank wants a program to manage customer accounts, deposits, and withdrawals.

## Requirements

Create the following functions:
- `create_account(accounts)`
- `deposit(accounts)`
- `withdraw(accounts)`
- `check_balance(accounts)`
- `display_accounts(accounts)`

The program should:

- Ask for the number of accounts to create.
- Store each account as a dictionary with an account holder's name, account number, and balance, e.g. `{"name": "Sarah", "account_number": 1001, "balance": 0}`.
- Account numbers should be generated automatically, starting from 1001 and increasing by 1 for each new account.
- Display a menu:
  ```
  1. View All Accounts
  2. Deposit Money
  3. Withdraw Money
  4. Check Balance
  5. Exit
  ```

If a user deposits money:
- Ask for the account number.
- Check if the account exists.
- Ask for the deposit amount.
- Validate the amount is positive.
- Add it to that account's balance.

If a user withdraws money:
- Ask for the account number.
- Check if the account exists.
- Ask for the withdrawal amount.
- Validate the amount is positive and does not exceed the current balance.
- Subtract it from that account's balance.

If a user checks balance:
- Ask for the account number.
- Display that account's current balance.

Before exiting, display:
- Total number of accounts
- Total amount of money currently held across all accounts
- The account with the highest balance

## Concepts Tested
- Dictionaries
- Lists
- Functions
- Loops
- Conditional statements
- Variables
- User input
- List/dictionary manipulation
