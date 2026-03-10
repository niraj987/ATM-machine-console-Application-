from flask import Flask, request, jsonify, render_template
import uuid
import datetime

app = Flask(__name__)

# Multi-user dummy database structured by Account Number
users_db = {
    "1000000001": {
        "Name": "Niraj Kumar",
        "Mobile No.": "12457836",
        "ATM pin": "9876",
        "Balance": 50000,
        "Bank Name": "State Bank of India",
        "Is_Blocked": False,
        "Daily_Limit": 20000,
        "Daily_Withdrawn": 0,
        "Transaction History": []
    },
    "1000000002": {
        "Name": "Raj Sharma",
        "Mobile No.": "98765432",
        "ATM pin": "1234",
        "Balance": 10000,
        "Bank Name": "HDFC Bank",
        "Is_Blocked": False,
        "Daily_Limit": 20000,
        "Daily_Withdrawn": 0,
        "Transaction History": []
    }
}

def generate_receipt_details(type, amount, balance, extra_info=None):
    receipt = {
        "transaction_id": str(uuid.uuid4())[:8].upper(),
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": type,
        "amount": amount,
        "balance": balance
    }
    if extra_info:
        receipt["extra_info"] = extra_info
    return receipt

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/user_info', methods=['POST'])
def get_user_info():
    data = request.json
    acc_no = data.get('account')
    if acc_no not in users_db:
        return jsonify({"status": "fail", "message": "Account not found"}), 404
        
    user = users_db[acc_no]
    if user["Is_Blocked"]:
        return jsonify({"status": "blocked"}), 403
        
    return jsonify({
        "name": user["Name"],
        "bank_name": user["Bank Name"],
        "mobile": user["Mobile No."],
        "account": acc_no
    })

@app.route('/api/verify_pin', methods=['POST'])
def verify_pin():
    data = request.json
    acc_no = data.get('account')
    pin = data.get('pin')
    
    if acc_no not in users_db:
         return jsonify({"status": "fail", "message": "Invalid Account Number"})
         
    user = users_db[acc_no]
    if user["Is_Blocked"]:
        return jsonify({"status": "blocked"})
        
    if pin == user["ATM pin"]:
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "fail", "message": "Invalid PIN"})

@app.route('/api/balance', methods=['POST'])
def get_balance():
    acc_no = request.json.get('account')
    user = users_db.get(acc_no)
    if not user: return jsonify({"status": "fail"}), 404
    if user["Is_Blocked"]: return jsonify({"status": "blocked"}), 403
    return jsonify({"balance": user["Balance"]})

@app.route('/api/withdraw', methods=['POST'])
def withdraw():
    data = request.json
    acc_no = data.get('account')
    amount = data.get('amount')
    
    user = users_db.get(acc_no)
    if not user: return jsonify({"status": "fail"}), 404

    try:
        amount = float(amount)
    except ValueError:
        return jsonify({"status": "fail", "message": "Invalid amount"})

    if amount <= 0:
        return jsonify({"status": "fail", "message": "Amount must be greater than zero"})

    if user["Is_Blocked"]:
        return jsonify({"status": "blocked"}), 403
        
    if amount > user["Balance"]:
        return jsonify({"status": "insufficient", "message": "Insufficient Balance"})
        
    if user["Daily_Withdrawn"] + amount > user["Daily_Limit"]:
        return jsonify({"status": "fail", "message": f"Daily limit of ₹{user['Daily_Limit']} exceeded."})

    user["Balance"] -= amount
    user["Daily_Withdrawn"] += amount
    user["Transaction History"].insert(0, f"Withdrew: ₹{amount}")
    
    receipt = generate_receipt_details("Withdrawal", amount, user["Balance"])
    return jsonify({"status": "success", "balance": user["Balance"], "receipt": receipt})

@app.route('/api/deposit', methods=['POST'])
def deposit():
    data = request.json
    acc_no = data.get('account')
    amount = data.get('amount')
    
    user = users_db.get(acc_no)
    if not user: return jsonify({"status": "fail"}), 404

    try:
        amount = float(amount)
    except ValueError:
        return jsonify({"status": "fail", "message": "Invalid amount"})

    if amount <= 0:
        return jsonify({"status": "fail", "message": "Amount must be greater than zero"})
        
    if user["Is_Blocked"]:
        return jsonify({"status": "blocked"}), 403
    
    user["Balance"] += amount
    user["Transaction History"].insert(0, f"Deposited: ₹{amount}")
    
    receipt = generate_receipt_details("Deposit", amount, user["Balance"])
    return jsonify({"status": "success", "balance": user["Balance"], "receipt": receipt})

@app.route('/api/transfer', methods=['POST'])
def transfer():
    data = request.json
    sender_acc = data.get('account')
    target_acc = data.get('target_account')
    amount = data.get('amount')
    
    sender = users_db.get(sender_acc)
    target = users_db.get(target_acc)
    
    if not sender: return jsonify({"status": "fail"}), 404
    if not target: return jsonify({"status": "fail", "message": "Target Account not found"})
    if sender_acc == target_acc: return jsonify({"status": "fail", "message": "Cannot transfer to self"})

    try:
        amount = float(amount)
    except ValueError:
        return jsonify({"status": "fail", "message": "Invalid amount"})

    if amount <= 0: return jsonify({"status": "fail", "message": "Invalid amount"})
    if sender["Is_Blocked"]: return jsonify({"status": "blocked"}), 403
    if target["Is_Blocked"]: return jsonify({"status": "fail", "message": "Target account blocked"})
        
    if amount > sender["Balance"]:
        return jsonify({"status": "insufficient", "message": "Insufficient Balance"})
        
    if sender["Daily_Withdrawn"] + amount > sender["Daily_Limit"]:
        return jsonify({"status": "fail", "message": f"Daily transfer limit of ₹{sender['Daily_Limit']} exceeded."})

    # Execute Transfer
    sender["Balance"] -= amount
    sender["Daily_Withdrawn"] += amount
    target["Balance"] += amount
    
    # Audit Logs
    sender["Transaction History"].insert(0, f"Transfer To ({target_acc}): ₹{amount}")
    target["Transaction History"].insert(0, f"Transfer From ({sender_acc}): ₹{amount}")
    
    receipt = generate_receipt_details("Bank Transfer", amount, sender["Balance"], extra_info=f"To: {target['Name']} ({target_acc})")
    
    return jsonify({"status": "success", "balance": sender["Balance"], "receipt": receipt})

@app.route('/api/change_pin', methods=['POST'])
def change_pin():
    data = request.json
    acc_no = data.get('account')
    old_pin = data.get('old_pin')
    new_pin = data.get('new_pin')
    
    user = users_db.get(acc_no)
    if not user: return jsonify({"status": "fail"}), 404

    if user["Is_Blocked"]:
        return jsonify({"status": "blocked"}), 403
    if old_pin == user["ATM pin"]:
        user["ATM pin"] = new_pin
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "fail", "message": "Incorrect Old PIN"})

@app.route('/api/block_card', methods=['POST'])
def block_card():
    acc_no = request.json.get('account')
    user = users_db.get(acc_no)
    if not user: return jsonify({"status": "fail"}), 404
    
    user["Is_Blocked"] = True
    return jsonify({"status": "blocked"})

@app.route('/api/history', methods=['POST'])
def get_history():
    acc_no = request.json.get('account')
    user = users_db.get(acc_no)
    if not user: return jsonify({"status": "fail"}), 404
    
    if user["Is_Blocked"]:
        return jsonify({"status": "blocked"}), 403
    return jsonify({"history": user["Transaction History"]})

if __name__ == '__main__':
    app.run(debug=True)
