import json


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


# Login as a user
def login():
    username = input("Enter your username:")
    password = input("Enter your password:")

    # Look for user in database
    with open('users.json', "r") as file:
        data = json.load(file)
        is_registered = False

        # Check if user exists
        for entry in data:
            if entry["username"] == username:
                is_registered = True
                break

        # If user exists, check if password is correct
        if is_registered:
            for entry in data:
                if entry["username"] == username and entry["password"] == password:
                    print("Successfully logged in")
                    return {"username": entry["username"], "wallet": entry["wallet"]}
            print("Either username or password were incorrect")
            return None
        else:
            # If user does not exist, ask if they want to register
            print("User does not exist. Would you like to register?")
            register = input("Enter Y/N:")
            if register == "Y":
                new_pass = input("Enter a password:")

                # Check if password is valid
                if not check_password(new_pass):
                    return None

                data.append({"username": username, "password": new_pass, "wallet": 0})
                with open('users.json', 'w') as outfile:
                    json.dump(data, outfile)
            else:
                return None
