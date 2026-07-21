# Atm Banking system problem

# Functions

def deposit(balance, amount):
    balance = balance + amount
    return balance

def withdraw(balance, amount):
    if amount <= balance:
        balance = balance - amount
        print("Withdrawal successful! ")
        
    else:
        print("Insufficient balance!")
    
    return balance

def check_balance(balance):
    print("current balance: ", balance)        
    
    
def display_menu():
    print("\n=======ATM MENU=======")    
    print("1. Deposit")
    print("2. Withdraw")
    print("3. Check balance")
    print("4. Exit")
      

#customers details
customer_name = input("Enter customer name: ")
account_number = input("Enter account number: ")
balance = int(input("Enter initial balance: "))

deposit_count = 0
withdrawal_count = 0

#read choice
while True:
    display_menu()
    
    choice = int(input("Enter your choice: "))
    
    if choice == 1:
        amount = int(input("Enter amount to deposit: "))
        balance = deposit(balance, amount)
        deposit_count += 1
        print("Deposit successful.")
        
    elif choice == 2:
        amount = int(input("Enter amount to withdraw: "))
        old_balance = balance
        balance = withdraw(balance, amount) 
        
        #count only successful withdrawals   
    
        if balance != old_balance:
            withdrawal_count += 1
        
    elif choice == 3:
        check_balance(balance)    
        
    elif choice == 4:
        print("customer name:", customer_name)
        print("Account number", account_number)
        print("Final account balance:", balance) 
        print("Total number of deposits:", deposit_count)
        print("Total number of withdrawals:", withdrawal_count)
        break
        
    else:
        print("invalid choice! please select 1, 2, 3, or 4.")    
        
        
        