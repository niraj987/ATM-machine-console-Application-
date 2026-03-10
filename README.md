# 🏦 Modern Smart ATM Web Application

A fully functional, elegantly designed ATM interface built with a **Python Flask** backend and a **Vanilla JS/CSS** frontend. This project simulates a real-world ATM with multi-user authentication, real-time balance tracking, interactive transaction receipts, strict daily limits, and dynamic inter-account bank transfers.

![Premium Glassmorphism Design](https://img.shields.io/badge/UI-Glassmorphism-6366f1.svg)
![Python](https://img.shields.io/badge/Backend-Python_Flask-3776AB?logo=python&logoColor=white)
![Frontend](https://img.shields.io/badge/Frontend-HTML/CSS/JS-E34F26?logo=html5)

## ✨ Key Features

- **🔐 Multi-User Authentication**: Secure login system requiring an Account Number and a 4-digit PIN.
- **💸 Real-Time Transactions**: Instantly process Cash Withdrawals and Deposits.
- **🏦 Bank Transfers**: Instantly send money to other valid accounts within the system.
- **🛑 Daily Limits**: Built-in fraud prevention enforcing a strict ₹20,000 daily withdrawal & transfer limit per account.
- **🧾 Smart Receipts**: Beautifully formatted receipts for every successful transaction including auto-generated Transaction IDs, timestamps, and remaining balances. (Supports physical printing via native browser print).
- **📝 Audit History**: A detailed, scrollable transaction history logging every credit and debit to the account.
- **⚙️ Account Settings**: Safely change user PINs or irreversibly block compromised cards directly from the ATM UI.
- **🎨 Premium UI/UX**: State-of-the-art "Glassmorphism" design with smooth CSS transitions, toast notification feedback, and a fully responsive grid.

## 🛠️ Technology Stack

* **Backend**: Python 3, Flask REST API
* **Frontend**: HTML5, CSS3 (Vanilla), JavaScript (ES6+ Fetch API)
* **Icons**: FontAwesome 6

## 🚀 How to Run Locally

1. **Clone the Repository**
   ```bash
   git clone <your-github-repo-url>
   cd "ATM using flask"
   ```

2. **Install Dependencies**
   Ensure you have Python installed, then install the required `flask` package:
   ```bash
   pip install flask
   ```

3. **Start the Flask Server**
   ```bash
   python app.py
   ```

4. **Open the Application**
   Open your preferred web browser and navigate to:
   ```text
   http://127.0.0.1:5000
   ```

## 🧪 Demo Accounts

The database runs in-memory. You can test the application using the following pre-configured dummy accounts:

| User Name   | Account Number | PIN  | Initial Balance | Bank Name |
| :---        | :---           | :--- | :---            | :---      |
| Niraj Kumar | `1000000001`   | `9876` | ₹ 50,000      | State Bank of India |
| Raj Sharma  | `1000000002`   | `1234` | ₹ 10,000      | HDFC Bank |


## 📂 Project Structure

```text
├── app.py                  # Main Flask backend server and API routes
├── templates/
│   └── index.html          # Main Single-Page Application (SPA) HTML view
├── static/
│   ├── style.css           # Vanilla CSS implementing Glassmorphism & Responsiveness
│   └── script.js           # Client-side logic for API requests and DOM manipulation
└── README.md               # Project documentation
```

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).
