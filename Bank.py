import re
import json

def check_pass_cond(password):
    pattern = re.compile(r'^(?=.*[a-z])(?=.*\d)(?=.*[A-Z])(?=.*[\W_])[a-zA-Z0-9\W_]{6,12}$')

    if re.match(pattern, password):
        return True
    else:
        return False
    
def welcome_message():
    while True:
        print("""Welcome to the simple banking system!
            1. Create an account
            2. Log in
            3. Exit""")
        answer = int(input("Enter your choice:"))
        match answer:
            case 1:
                create_user_screen()
            case 2:
                log_in_screen()
            case _:
                break


def create_user_screen():
    username =  input("Enter Username: ")
    password =  input("Enter Password: ")
    if check_pass_cond(password) == False:
        print("""Your password didnt meet the conditions!
            • At least 1 letter between [a-z]
            • At least 1 number between [0-9]
            • At least 1 letter between [A-Z]
            • At least 1 character from [#@%]
            • Minimum length of transaction password: 6
            • Maximum length of transaction password: 12""")
        create_user_screen()
    elif username_exists(username):
        print(f"The username '{username}' already exists. Please choose a different username.")
        create_user_screen()
    else:
        balance = 0
        user = {
            "username" : username,
            "password" : password,
            "balance" : int(balance)
        }
        try:
            with open("User.json", "r") as file:
                data = json.load(file)
            
            data["users"].append(user)

            with open("User.json", "w") as file:
                json.dump(data, file, indent=2)
            print(f"The user {username} has been succesfully added!")
        except Exception as e:
            print(f"Error: {e}") 
      

def username_exists(username):
    try:
        with open("User.json", "r") as inputfile:
            data = json.load(inputfile)

        users = data.get("users", [])
        for user in users:
            if user.get("username") == username:
                return True

    except Exception as e:
        print(f"Error: {e}")

    return False

def username_not_found(username):
    try:
        with open("User.json", "r") as inputfile:
            data = json.load(inputfile)

        users = data.get("users", [])
        for user in users:
            if user.get("username") == username:
                return False

    except Exception as e:
        print(f"Error: {e}")
    print("Username not found!")
    return True

def deposit_balance(username, amount):
    try:
        with open("User.json", "r") as file:
            data = json.load(file)

        users = data.get("users", [])
        for user in users:
            if user.get("username") == username:
                current_balance = user.get("balance", 0)
                new_balance = current_balance + amount
                user["balance"] = new_balance

                with open("User.json", "w") as file:
                    json.dump(data, file, indent=2)

                print(f"Deposit successful! New balance for {username}: {new_balance}")
                return  # Exit the function after successful deposit

        print(f"User '{username}' not found.")
    except Exception as e:
        print(f"Error: {e}")

def withdraw_balance(username, amount):
    try:
        with open("User.json", "r") as file:
            data = json.load(file)

        users = data.get("users", [])
        for user in users:
            if user.get("username") == username:
                current_balance = user.get("balance", 0)
                new_balance = current_balance - amount
                if new_balance < 0:
                    print("Insufficient balance!")
                    return  # Exit the function if balance is insufficient
                
                user["balance"] = new_balance

                with open("User.json", "w") as file:
                    json.dump(data, file, indent=2)

                print(f"Withdraw successful! New balance for {username}: {new_balance}")
                return  # Exit the function after successful withdrawal

        print(f"User '{username}' not found.")
    except Exception as e:
        print(f"Error: {e}")

def view_balance(username):
    try:
        with open("User.json", "r") as file:
            data = json.load(file)

        users = data.get("users", [])
        for user in users:
            if user.get("username") == username:
                current_balance = user.get("balance", 0)
                print(f"Balance for {username} is: {current_balance}")
                return  # Exit the function after finding the user

        print(f"User '{username}' not found.")
    except Exception as e:
        print(f"Error: {e}")

def logged_in_user(user):
    while True:
        print(f"""Welcome {user}
                1. Deposit Money
                2. Withdraw Money
                3. View Balance
                4. Log Out""")
        answer = int(input("Enter your choice:"))
        match answer:
            case 1:
                amount = int(input("How much do you want to deposit?: "))
                deposit_balance(user, amount)
                
            case 2:
                amount = int(input("How much do you want to withdraw?: "))
                withdraw_balance(user, amount)
               
            case 3:
                view_balance(user)
               
            case _:
                break

def log_in_screen():
    print("Enter your credentials below to login.")
    username = input("Enter Username: ")
    while username_not_found(username):
        username = input("Enter Username: ")
    
    password = input("Enter Password: ")

    try:
        with open("User.json", "r") as checkfile:
            data = json.load(checkfile)
            for user in data.get("users", []):
                if user.get("username") == username and user.get("password") == password:
                    logged_in_user(username)
                    return  # Exit the function after successful login

            print("Invalid username or password. Please try again.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    welcome_message()