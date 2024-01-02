import json
from typing import Union
from login import check_password


# Alter the details for a user
# Returns none or edited entry
def change_details(entry):
    print("\n")
    print("Welcome to the store!\n")
    answer = input("Do you wish to change you account details? (Y/N) :\n")
    if answer == "Y":
        detail = input(
            "Which detail do you want to alter? (p: password, a: address, ph: phone, e: email, c: credit card):\n"
        )

        #Switch statement for the different details

        if detail == "p":
            altered_pass = input("Enter a new password:")
            # Check if password is valid
            if not check_password(altered_pass):
                return None
            entry["password"] = altered_pass

        elif detail == "a":
            altered_address = input("Enter a new street address:")
            entry["address"] = altered_address
        elif detail == "ph":
            altered_phone = input("Enter a new phone number:")
            entry["phone"] = altered_phone
        elif detail == "e":
            altered_email = input("Enter a new email address:")
            entry["email"] = altered_email
        elif detail == "c":
            new_credit = {
            "number": input("Enter a new credit card number:"),
            "expiry": input("Enter a new credit card expiry date:"),
            "cvv": input("Enter a new credit card CVV:"),
            }
            entry["credit"] = new_credit
        else:
            return None


        print("The details have successfully been changed to: " + entry)

    else:
        return None
