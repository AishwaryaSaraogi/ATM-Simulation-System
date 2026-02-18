import json
import os

# --- Constants & Configuration ---
DATA_FILE = "accounts.json"
MAX_ATTEMPTS = 3  # PIN-based authentication with lockout [cite: 6]

def load_data():
    """Integrate JSON read for persistent storage[cite: 15]."""
    if not os.path.exists(DATA_FILE):
        # Initial design using nested dictionaries for account storage [cite: 10]
        initial_data = {
            "101": {"name": "Alice", "pin": "1234", "balance": 5000.0, "history": []},
            "102": {"name": "Bob", "pin": "5678", "balance": 2500.0, "history": []}
        }
        save_data(initial_data)
        return initial_data
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    """Integrate JSON write for persistent storage[cite: 15]."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def log_transaction(account, message):
    """Add mini statement using list-based logs[cite: 14]."""
    account["history"].append(message)
    if len(account["history"]) > 10:  # Keep last 5-10 transactions [cite: 6]
        account["history"].pop(0)

def authenticate(data):
    """Build authentication function with PIN retries[cite: 11]."""
    print("\n--- Welcome to Python ATM ---")
    acc_id = input("Enter Account Number: ")
    
    if acc_id not in data:
        print("Account not found.")
        return None

    attempts = 0
    while attempts < MAX_ATTEMPTS:
        pin = input(f"Enter PIN ({MAX_ATTEMPTS - attempts} attempts left): ")
        if data[acc_id]["pin"] == pin:
            print(f"Login Successful! Welcome, {data[acc_id]['name']}.")
            return acc_id
        else:
            attempts += 1
            print("Incorrect PIN.")
    
    print("Lockout: Too many failed attempts.") # PIN lockout [cite: 6]
    return None

def main():
    data = load_data()
    current_acc = authenticate(data)
    
    if not current_acc:
        return

    user = data[current_acc]

    # Create ATM menu with loops and routing [cite: 12]
    while True:
        print("\n--- ATM Menu ---")
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer")
        print("5. Mini Statement")
        print("6. Exit")
        
        # Add error handling for user inputs [cite: 16]
        choice = input("Select an option: ")

        if choice == "1":
            print(f"Current Balance: ${user['balance']}")

        elif choice == "2":
            try:
                amount = float(input("Enter deposit amount: "))
                if amount > 0:
                    user["balance"] += amount
                    log_transaction(user, f"Deposited: ${amount}")
                    print(f"Deposit successful! New balance: ${user['balance']}")
                else:
                    print("Invalid amount.")
            except ValueError:
                print("Please enter a numeric value.")

        elif choice == "3":
            try:
                amount = float(input("Enter withdrawal amount: "))
                if 0 < amount <= user["balance"]:
                    user["balance"] -= amount
                    log_transaction(user, f"Withdrew: ${amount}")
                    print(f"Withdrawal successful! Remaining balance: ${user['balance']}")
                else:
                    print("Insufficient funds or invalid amount.")
            except ValueError:
                print("Please enter a numeric value.")

        elif choice == "4":
            target_id = input("Enter recipient account number: ")
            if target_id in data and target_id != current_acc:
                try:
                    amount = float(input("Enter transfer amount: "))
                    if 0 < amount <= user["balance"]:
                        user["balance"] -= amount
                        data[target_id]["balance"] += amount
                        log_transaction(user, f"Transferred ${amount} to {target_id}")
                        log_transaction(data[target_id], f"Received ${amount} from {current_acc}")
                        print("Transfer successful!")
                    else:
                        print("Insufficient funds.")
                except ValueError:
                    print("Invalid amount.")
            else:
                print("Recipient account not found.")

        elif choice == "5":
            print("\n--- Mini Statement ---")
            for record in user["history"]:
                print(record)
            if not user["history"]:
                print("No transactions yet.")

        elif choice == "6":
            save_data(data)
            print("Thank you for using our ATM. Goodbye!")
            break
        else:
            print("Invalid selection.")

if __name__ == "__main__":
    main()