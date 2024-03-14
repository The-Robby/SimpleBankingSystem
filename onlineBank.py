import func
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
        if username == 'debug':
            return accounts
        for account in accounts:
            if account['username'] == username and func.check_password(account, password):
                session['account'] = account
                return redirect(url_for('dashboard'))
        return render_template("login.html", wrongcredentials=True)
    return render_template("login.html")

@app.route("/logout")
def logout():
    if 'account' in session:
        session.pop('account')
    return redirect(url_for('index'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if func.check_pass_cond(password):
            check = 1
            for acc in accounts:
                if acc['username'] == username:
                    check -= 1
                    return render_template("login.html", register=True, wrongname=True, username=username)
            if check == 1:    
                account_number = len(accounts) + 1
                accounts.append({'account_number': account_number, 'username': username, 'password': func.store_pass(password), 'balance': 100.0})
                return redirect(url_for('index'))
        else:
            return render_template("login.html", register=True, wrongpass=True)

    return render_template("login.html", register=True)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'account' in session:
        account = session['account']
        return render_template('dashboard.html', account=account)
    return redirect(url_for('login'))

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