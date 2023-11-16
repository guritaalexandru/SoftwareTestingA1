def logout(cart):

    #logout if cart is empty
    if len(cart.items) == 0:
        return True

    #Retrieve cart items and ten asking for confirmation of logout
    print("Your cart is not empty.You have following items")
    for i in cart.retrieve_item():
        print(i.get_product())

    logout_confirmation = input("Do you still want to logout? (Y/N): ").lower()

    #Confirming whether to logout or not
    if logout_confirmation.lower() == "y":
        cart.clear_items()
        return True
    else:
        return False
