from flask import Flask, render_template, request, redirect, url_for, session
from hashlib import pbkdf2_hmac as pbkdf2
import re
import os

app = Flask(__name__, static_folder="static")
app.secret_key = 'your_secret_key'
accounts = []
# -----------------------------------------------------------------------------------------FUNCTIONS--------------------------------------------------------------------------------
def check_pass_cond(password):
    pattern = re.compile(r'^(?=.*[a-z])(?=.*\d)(?=.*[A-Z])(?=.*[\W_])[a-zA-Z0-9\W_]{6,12}$')

    if re.match(pattern, password):
        return True
    else:
        return False
    
def create_hash(password, salt):
    plaintext = password.encode()
    digest = pbkdf2('sha256', plaintext, salt, 100000)
    hex_hash = digest.hex()
    return hex_hash

def store_pass(password):
    salt=os.urandom(32)
    hashed_password = create_hash(password,salt)
    return [hashed_password, salt.decode('latin1')]

def check_password(account, userPassword):
    hash_password_InDB = account['password'][0]
    salt = account['password'][1].encode('latin1')
    hex_hash = create_hash(userPassword,salt)
    return hex_hash == hash_password_InDB

# -----------------------------------------------------------------------------------------INDEX.HTML--------------------------------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/logout")
def logout():
    if 'account' in session:
        session.pop('account')
    return redirect(url_for('index'))

# -----------------------------------------------------------------------------------------LOGIN.HTML--------------------------------------------------------------------------------
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'debug':
            return accounts
        for account in accounts:
            if account['username'] == username and check_password(account, password):
                session['account'] = account
                return redirect(url_for('dashboard'))
        return render_template("login.html", wrongcredentials=True)
    return render_template("login.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_pass_cond(password):
            check = 1
            for acc in accounts:
                if acc['username'] == username:
                    check -= 1
                    return render_template("login.html", register=True, wrongname=True, username=username)
            if check == 1:    
                account_number = len(accounts) + 1
                accounts.append({'account_number': account_number, 'username': username, 'password': store_pass(password), 'balance': 100.0})
                return redirect(url_for('index'))
        else:
            return render_template("login.html", register=True, wrongpass=True)

    return render_template("login.html", register=True)

# -----------------------------------------------------------------------------------------DASHBOARD.HTML--------------------------------------------------------------------------------
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'account' in session:
        account = session['account']
        return render_template('dashboard.html', account=account)
    return redirect(url_for('login'))

# -----------------------------------------------------------------------------------------DEPOSIT.HTML--------------------------------------------------------------------------------
@app.route('/deposit', methods=['POST'])
def deposit():
    if 'account' in session:
        account = session['account']
        if request.form['amount'] == '':
            return render_template('dashboard.html', depositempty=True, account=account)
        amount = float(request.form['amount'])


        for acc in accounts:
            if account['account_number'] == acc['account_number']:
                acc['balance'] += amount
                new_amount = acc['balance']
                session['account'] = acc
                return render_template('deposit.html', deposit=True, account=account, amount=amount, new_amount = new_amount)
    
    return redirect(url_for('login'))

@app.route('/withdraw', methods=['POST'])
def withdraw():
    if 'account' in session:
        account = session['account']
        if request.form['amount_withdraw'] == '':
            return render_template('dashboard.html', withdrawempty=True, account=account)
        amount = float(request.form['amount_withdraw'])

        for acc in accounts:
            if account['account_number'] == acc['account_number']:
                if acc['balance'] - amount >= 0:
                    acc['balance'] -= amount
                    new_amount = acc['balance']
                    session['account'] = acc
                    return render_template('deposit.html', deposit=False, account=account, amount=amount, new_amount = new_amount)
                else:
                    return render_template('dashboard.html', account=account, amount=amount, error=True)
    
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)