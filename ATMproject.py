user_information = {
    "Name": "Niraj Kumar",
    "Mobile No.": "12457836",
    "ATM pin": "9876",
    "Balance": 5000,
    "Bank Name": "State Bank of India",
    "Is_Blocked": False,
    "Transaction History": []
}

chances = 3
print("----------------------------------------------------------------")
print(f"--- Welcome to {user_information['Bank Name']} ATM ---")

while chances > 0:
    if user_information["Is_Blocked"]:
        print("\nACCESS DENIED: Your card is currently blocked.")
        break
    # pin entering
    pin_input = input("\nEnter your 4-digit PIN: ")
    if len(pin_input) != 4:
        print("Error: Please enter a valid 4-digit PIN.")
        continue
    if pin_input == user_information["ATM pin"]:
        is_running = True
        while is_running:
            print(f"\n--- HOME PAGE ({user_information['Name']}) ---")
            print(
                "1. Balance Check\n2. Withdraw Money\n3. Deposit Money\n4. Change PIN\n5. History\n6. Block Card\n7. Exit")
            choice = input("\nSelect (1-7): ")
            if choice == '1':
                print(f"Balance: ₹{user_information['Balance']}")
            elif choice == '2':
                amount = int(input("Amount to withdraw:₹ "))
                if amount <= user_information["Balance"]:
                    user_information["Balance"] -= amount
                    user_information["Transaction History"].append(f"Withdrew: ₹{amount}")
                    print(f"Success! New Balance: ₹{user_information['Balance']}")
                else:
                    print("Insufficient funds.")
            elif choice == '3':
                amount = int(input("Amount to deposit:₹ "))
                if amount >= 100 and amount % 100 == 0:
                    user_information["Balance"] += amount
                    user_information["Transaction History"].append(f"Deposited: ₹{amount}")
                    print(f"Success! New Balance: ₹{user_information['Balance']}")
                else:
                    print("Invalid amount.")
            elif choice == '4':
                old_pin = input("Enter current PIN: ")
                if old_pin == user_information["ATM pin"]:
                    new_pin = input("Enter new 4-digit PIN: ")
                    if new_pin == old_pin:
                        print("New PIN cannot be the same as old PIN.")
                    elif len(new_pin) == 4 and new_pin.isdigit():
                        user_information["ATM pin"] = new_pin
                        print("PIN updated!")
                    else:
                        print("Invalid format.")
                else:
                    print("Incorrect current PIN.")
            elif choice == '5':
                print("\n--- History ---")
                for entry in user_information["Transaction History"]: print(f"• {entry}")
                if not user_information["Transaction History"]: print("No records.")

            elif choice == '6':
                if input("Confirm block? (yes/no): ").lower() == 'yes':
                    user_information["Is_Blocked"] = True
                    print("Your card has been blocked.Contact to nearby branch.")
                    is_running = False
            elif choice == '7':
                is_running = False
            if is_running:
                if input("\nBack to Home Page? (y/n): ").lower() != 'y':
                    is_running = False
        break
    else:
        # This section only runs if the PIN is wrong
        chances -= 1
        if chances > 0:
            print(f"Incorrect PIN. Please enter the correct PIN. ({chances} attempts left)")
        else:
            user_information["Is_Blocked"] = True
            print("\nMaximum attempts reached. Card blocked.")
print("\n--- Thank you for using our services, visit again ------------")