# ATM-machine-console-Application-
This console-based Python banking app securely manages a single user's account via a dictionary (name, account number, balance, 4-digit PIN). It features:  3-strike PIN lockout Balance check Deposit (accepts only standard denominations: $10/$20/$50/$100) Withdrawal (checks funds + $20 multiples) PIN change (with current PIN verification) .

1. Project Objective
The primary objective of this project is the functional logic of an Automated Teller Machine (ATM). It aims to provide a secure environment for users to perform basic banking tasks such as balance inquiries, fund transfers (deposits/withdrawals), and account security management through a command-line interface.
2. Project Description
This software is a console-based program that manages a single user's bank account details using a Python dictionary. The system mimics real-world security protocols, including PIN validation and a "three-strike" lockout mechanism. It ensures data integrity by checking for sufficient funds during withdrawals and validating currency denominations during deposits.
3. Core Goals
Security: To protect user accounts via 4-digit PIN authentication.
Account Management: To allow real-time updates to account balances and security credentials.
User Experience: To provide a clear, menu-driven interface for easy navigation.
Error Handling: To prevent illegal operations (e.g., withdrawing more than the available balance or entering invalid PIN lengths).
________________________________________
4. Technical Specifications & Logic
4.1 Data Architecture
The project utilizes a dictionary-based structure to store user data, which allows  user to check balance, deposit money when retrieving user attributes:
Balance: Integer representing the current funds.
Is_Blocked: Boolean flag to control account access.
ATM pin: String value for security comparisons.
4.2 Key Features
Authentication Loop: A while loop combined with a chance’s variable limits the user to three attempts before the card is flagged as blocked.
Withdrawal Validation: * Condition: amount <= user_information["Balance"]
Deposit Constraints: * Condition: Minimum deposit of ₹500.
Condition: Must be in multiples of 100.
Self-Blocking Mechanism: A dedicated option for users to manually block their card in case of an emergency (theft/loss).
________________________________________
5. System Flowchart (Logical Steps)
Start: Display Bank Welcome message.
Verification: Check if Is_Blocked is True. If yes, terminate.
PIN Entry: User enters 4-digit PIN.
Invalid: Decrease chances. At 0, block card.
Valid: Proceed to Menu.
Operation Selection: * 1: Display Balance.
2: Subtract from Balance (if funds exist).
3: Add to Balance (if > 500 and multiple of 100).
4: Update PIN string.
5: Set Is_Blocked to True and Exit.
End: Display "Thank You" message and exit.
________________________________________

6. Future Enhancements
Persistent Storage: Integrating a SQL database or JSON file to save data after the program closes.
Multi-User Support: Transitioning from a single dictionary to a list of dictionaries or an Object-Oriented (OOP) approach.
GUI: Developing a Graphical User Interface using libraries like Tkinter or flask.



