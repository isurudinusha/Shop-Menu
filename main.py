import sqlite3
import order_history
import add_basket
import view_basket
import checkout
import clear_basket

# Connecting to the database and then asking the user to enter their ID.
db = sqlite3.connect("Orinoco.db")
cursor = db.cursor()
print("\nSuccessfully connected to Orinoco!")
shopper = False
shopper_id = 0
while not shopper:
    try:
        shopper_id = int(input("\nEnter your ID or 0 to exit: "))
        if shopper_id != 0:
            # Checking if the shopper_id exists in the database.
            sql_query = "SELECT * FROM shoppers WHERE shopper_id = ?"
            cursor.execute(sql_query, (shopper_id,))
            shopper = cursor.fetchone()
            if shopper:
                print("\nWelcome", shopper[2], shopper[3])
            else:
                print("This ID doesn't exist. Please try again!")

        else:
            db.close()
            exit()
    except ValueError:
        print("Please enter a valid ID...")


def exit_program(db, cursor, shopper_id):
    exit()


def menu():
    """
    It takes the user's input, and then runs the corresponding function from the functions dictionary
    """
    print("\nORINOCO - SHOPPER MAIN MENU")
    print("----------------------------------------------------------")
    user_input = 0
    while user_input > 6 or user_input==0:
        user_input = int(
            input(
                """
            
            1.	Display your order history
            2.	Add an item to your basket
            3.	View your basket
            4.	Clear your basket
            5.	Checkout
            6.	Exit

            Please enter your choice: """
            )
        )
    functions = {
        1: order_history.sql,
        2: add_basket.sql,
        3: view_basket.basket,
        4: clear_basket.delete,
        5: checkout.sql,
        6: exit_program,
    }
    functions[user_input](db, cursor, shopper_id)
    menu()


menu()
