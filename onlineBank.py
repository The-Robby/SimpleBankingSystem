import Bank
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__, static_folder="static")
app.secret_key = 'your_secret_key'


accounts = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        for account in accounts:
            if account['username'] == username and account['password'] == password:
                session['account'] = account
                return redirect(url_for('dashboard'))
        return render_template("flogin.html")
    return render_template("login.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if Bank.check_pass_cond(password):
            account_number = len(accounts) + 1
            accounts.append({'account_number': account_number, 'username': username, 'password': password, 'balance': 100.0})
            return redirect(url_for('index'))
        else:
            return render_template("fregister.html")

    return render_template("register.html")

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'account' in session:
        account = session['account']
        return render_template('dashboard.html', account=account)
    return redirect(url_for('login'))

@app.route('/deposit', methods=['POST'])
def deposit():
    if 'account' in session:
        amount = float(request.form['amount'])
        account = session['account']

        for acc in accounts:
            if account['account_number'] == acc['account_number']:
                acc['balance'] += amount
                session['account'] = acc
                return render_template('deposit.html', account=account, amount=amount)
    
    return redirect(url_for('login'))

@app.route('/withdraw', methods=['POST'])
def withdraw():
    if 'account' in session:
        amount = float(request.form['amount_withdraw'])
        account = session['account']

        for acc in accounts:
            if account['account_number'] == acc['account_number']:
                if acc['balance'] - amount >= 0:
                    acc['balance'] -= amount
                    session['account'] = acc
                    return render_template('deposit.html', account=account, amount=amount)
                else:
                    return "Not enough money to withdraw!"
    
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)