// Utility function to show Toast notifications
function showToast(message, type = 'success') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `<i class="fa-solid fa-${type === 'success' ? 'check-circle' : 'circle-exclamation'}"></i> ${message}`;
    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(-20px)';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Global Headers for JSON requests
const headers = { 'Content-Type': 'application/json' };
let currentAccount = null;

// Screen Navigation
function showScreen(screenId) {
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    document.getElementById(screenId).classList.add('active');

    // Clear inputs on navigate
    document.getElementById('withdraw-amount').value = '';
    document.getElementById('deposit-amount').value = '';
    document.getElementById('transfer-amount').value = '';
    document.getElementById('transfer-target').value = '';
    document.getElementById('old-pin').value = '';
    document.getElementById('new-pin').value = '';

    if (screenId === 'dashboard-screen' && currentAccount) {
        fetchBalance();
    }
}

// Display Receipt Screen
function showReceipt(receipt) {
    document.getElementById('receipt-bank').innerText = document.getElementById('bank-name').innerText;
    document.getElementById('rec-date').innerText = receipt.date;
    document.getElementById('rec-id').innerText = receipt.transaction_id;
    document.getElementById('rec-type').innerText = receipt.type;
    document.getElementById('rec-amt').innerText = `₹ ${receipt.amount.toLocaleString('en-IN', { minimumFractionDigits: 2 })}`;
    document.getElementById('rec-bal').innerText = `₹ ${receipt.balance.toLocaleString('en-IN', { minimumFractionDigits: 2 })}`;

    if (receipt.extra_info) {
        document.getElementById('rec-extra-row').style.display = 'flex';
        document.getElementById('rec-extra').innerText = receipt.extra_info;
    } else {
        document.getElementById('rec-extra-row').style.display = 'none';
    }

    showScreen('receipt-screen');
}

// Logic implementations
document.getElementById('login-btn').addEventListener('click', async () => {
    const acc = document.getElementById('acc-input').value;
    const pin = document.getElementById('pin-input').value;

    if (!acc || pin.length !== 4) {
        showToast('Valid Account and 4-digit PIN required', 'error');
        return;
    }

    try {
        const res = await fetch('/api/verify_pin', {
            method: 'POST',
            headers,
            body: JSON.stringify({ account: acc, pin: pin })
        });
        const data = await res.json();

        if (data.status === 'success') {
            currentAccount = acc;
            document.getElementById('active-acc-disp').innerText = currentAccount;
            showToast('Login Successful');
            fetchUserInfo();
            showScreen('dashboard-screen');
        } else if (data.status === 'blocked') {
            showToast('Card is Blocked. Contact Bank.', 'error');
        } else {
            showToast(data.message || 'Invalid Credentials', 'error');
        }
    } catch (e) {
        showToast('Server error', 'error');
    }
});

async function fetchUserInfo() {
    try {
        const res = await fetch('/api/user_info', {
            method: 'POST',
            headers,
            body: JSON.stringify({ account: currentAccount })
        });
        const data = await res.json();
        if (data.status !== 'blocked') {
            document.getElementById('user-name').innerText = data.name;
            document.getElementById('bank-name').innerText = data.bank_name;
        }
    } catch (e) { }
}

async function fetchBalance() {
    try {
        const res = await fetch('/api/balance', {
            method: 'POST',
            headers,
            body: JSON.stringify({ account: currentAccount })
        });
        const data = await res.json();
        if (data.status !== 'blocked') {
            document.getElementById('current-balance').innerText = `₹ ${data.balance.toLocaleString('en-IN', { minimumFractionDigits: 2 })}`;
        }
    } catch (e) { }
}

function setWithdrawAmount(amt) {
    const input = document.getElementById('withdraw-amount');
    input.value = (parseFloat(input.value || 0) + amt);
}

async function handleWithdraw() {
    const amount = document.getElementById('withdraw-amount').value;
    if (!amount || amount <= 0) {
        showToast('Enter a valid amount', 'error');
        return;
    }

    try {
        const res = await fetch('/api/withdraw', {
            method: 'POST',
            headers,
            body: JSON.stringify({ account: currentAccount, amount: parseFloat(amount) })
        });
        const data = await res.json();

        if (data.status === 'success') {
            showToast(`Successfully withdrew ₹${amount}`);
            showReceipt(data.receipt);
        } else {
            showToast(data.message || 'Withdrawal failed', 'error');
        }
    } catch (e) { showToast('Error processing request', 'error'); }
}

async function handleDeposit() {
    const amount = document.getElementById('deposit-amount').value;
    if (!amount || amount <= 0) {
        showToast('Enter a valid amount', 'error');
        return;
    }

    try {
        const res = await fetch('/api/deposit', {
            method: 'POST',
            headers,
            body: JSON.stringify({ account: currentAccount, amount: parseFloat(amount) })
        });
        const data = await res.json();

        if (data.status === 'success') {
            showToast(`Successfully deposited ₹${amount}`);
            showReceipt(data.receipt);
        } else {
            showToast(data.message || 'Deposit failed', 'error');
        }
    } catch (e) { showToast('Error processing request', 'error'); }
}

async function handleTransfer() {
    const target = document.getElementById('transfer-target').value;
    const amount = document.getElementById('transfer-amount').value;

    if (!target || !amount || amount <= 0) {
        showToast('Valid Destination and Amount required', 'error');
        return;
    }

    try {
        const res = await fetch('/api/transfer', {
            method: 'POST',
            headers,
            body: JSON.stringify({ account: currentAccount, target_account: target, amount: parseFloat(amount) })
        });
        const data = await res.json();

        if (data.status === 'success') {
            showToast(`Successfully transferred ₹${amount}`);
            showReceipt(data.receipt);
        } else {
            showToast(data.message || 'Transfer failed', 'error');
        }
    } catch (e) { showToast('Error processing request', 'error'); }
}


async function fetchHistory() {
    const list = document.getElementById('history-list');
    list.innerHTML = '<p style="text-align:center; color: var(--text-muted)">Loading...</p>';

    try {
        const res = await fetch('/api/history', {
            method: 'POST',
            headers,
            body: JSON.stringify({ account: currentAccount })
        });
        const data = await res.json();

        if (data.history && data.history.length > 0) {
            list.innerHTML = '';
            data.history.forEach(item => {
                const isDeposit = item.includes('Deposited') || item.includes('Transfer From');
                const isTransferOut = item.includes('Transfer To');
                const parts = item.split(': ');

                let iconHtml = '';
                if (isTransferOut) {
                    iconHtml = '<i class="fa-solid fa-arrow-right-from-bracket"></i>';
                } else if (isDeposit) {
                    iconHtml = '<i class="fa-solid fa-arrow-down"></i>';
                } else {
                    iconHtml = '<i class="fa-solid fa-arrow-up"></i>';
                }

                const html = `
                    <div class="history-item">
                        <div class="history-icon ${isDeposit ? 'deposit' : 'withdraw'}">
                            ${iconHtml}
                        </div>
                        <div class="history-details" style="font-size: 0.9rem;">
                            <p>${parts[0]}</p>
                            <span>${new Date().toLocaleDateString('en-IN')}</span>
                        </div>
                        <div style="font-weight:600; color: var(--${isDeposit ? 'success' : 'text-main'})">
                            ${isDeposit ? '+' : '-'}${parts[1]}
                        </div>
                    </div>
                `;
                list.insertAdjacentHTML('beforeend', html);
            });
        } else {
            list.innerHTML = '<p style="text-align:center; color: var(--text-muted)">No recent transactions</p>';
        }
    } catch (e) { list.innerHTML = 'Error loading history'; }
}

async function handleChangePin() {
    const oldPin = document.getElementById('old-pin').value;
    const newPin = document.getElementById('new-pin').value;

    if (oldPin.length !== 4 || newPin.length !== 4) {
        showToast('PIN must be 4 digits', 'error');
        return;
    }

    try {
        const res = await fetch('/api/change_pin', {
            method: 'POST',
            headers,
            body: JSON.stringify({ account: currentAccount, old_pin: oldPin, new_pin: newPin })
        });
        const data = await res.json();

        if (data.status === 'success') {
            showToast('PIN changed successfully');
            document.getElementById('old-pin').value = '';
            document.getElementById('new-pin').value = '';
        } else {
            showToast(data.message || 'Failed to change PIN', 'error');
        }
    } catch (e) { showToast('Error', 'error'); }
}

async function handleBlockCard() {
    if (!confirm("Are you SURE you want to block your card? This action is irreversible.")) return;

    try {
        const res = await fetch('/api/block_card', {
            method: 'POST',
            headers,
            body: JSON.stringify({ account: currentAccount })
        });
        const data = await res.json();
        if (data.status === 'blocked') {
            showToast('Card successfully BLOCKED', 'error');
            setTimeout(logout, 2000);
        }
    } catch (e) { }
}

function logout() {
    currentAccount = null;
    document.getElementById('acc-input').value = '';
    document.getElementById('pin-input').value = '';
    showScreen('login-screen');
    showToast('Logged out successfully');
}

// Add enter key support for login
document.getElementById('pin-input').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        document.getElementById('login-btn').click();
    }
});
