import json
from change_details import change_details


# Check if password is valid
def check_password(password):
    special_characters = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '{', '}', '|', ':', '"', '<', '>',
                          '?', '/', '\\']
    if not any(char.isupper() for char in password):
        print('Password should have at least one capital letter')
        return False
    if not any(char.isdigit() for char in password):
        print('Password should have at least one numeral')
        return False
    if len(password) < 8:
        print('Password should be of length 8 or more')
        return False
    if not any(char in special_characters for char in password):
        print('Password should have at least one special character')
        return False
    return True


def write_to_file(data):
    with open('users.json', 'w') as outfile:
        json.dump(data, outfile)


# Login as a user
def login():
    username = input("Enter your username:")
    password = input("Enter your password:")

    # Look for users in database
    with open('users.json', "r") as file:
        data = json.load(file)
        is_registered = False

        # Check if user exists and if password corresponds
        for entry in data:
            if entry["username"] == username:
                if entry["password"] == password:
                    print("Successfully logged in")
                    result = change_details(entry)
                    if result == None:
                        return {"username": entry["username"], "wallet": entry["wallet"]}
                    else:
                        entry = result
                        # Check if password is valid
                        if not check_password(entry["password"]):
                            return None
 
                        write_to_file(data)
                    return {"username": entry["username"], "wallet": entry["wallet"]}
                print("Either username or password were incorrect")
                return None

        # If user does not exist, ask if they want to register
        print("User does not exist. Would you like to register?")
        register = input("Enter Y/N:")
        if register == "Y":
            new_pass = input("Enter a password:")

            # Check if password is valid
            if not check_password(new_pass):
                return None
            
            new_address = input("Enter a street address:")
            new_phone = input("Enter a phone number:")
            new_email = input("Enter an email address:")
            new_credit = {"number": input("Enter a credit card number:"), "expiry": input("Enter a credit card expiry date:"), "cvv": input("Enter a credit card CVV:")}



            data.append({"username": username, "password": new_pass, "wallet": 0, "address": new_address, "phone": new_phone, "email": new_email, "credit": new_credit})
            write_to_file(data)

            print("Successfully registered")
            return {"username": username, "wallet": 0}
        else:
            return None
