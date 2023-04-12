from datetime import datetime


def sql(db, cursor, shopper_id):
    # This is a SQL query that is being executed. The query is selecting the category_id and
    # category_description from the categories table and ordering them by category_description. The result
    # of the query is being stored in the categories variable. The category_id variable is being set to
    # the result of the _display_options function.
    select_category = """
        SELECT category_id, category_description FROM categories
        ORDER BY category_description
        """
    cursor.execute(select_category)
    categories = cursor.fetchall()
    category_id = _display_options(categories, "Product Categories", "category")

    # This is a SQL query that is being executed. The query is selecting the product_id and
    # product_description from the products table and ordering them by product_description. The result
    # of the query is being stored in the products variable. The product_id variable is being set to
    # the result of the _display_options function.
    select_product = """
        SELECT product_id, product_description FROM products
        WHERE category_id = ?
        ORDER BY product_description
        """
    cursor.execute(
        select_product,
        (category_id,),
    )
    products = cursor.fetchall()
    product_id = _display_options(products, "Products", "proudct")

    # This is a SQL query that is being executed. The query is selecting the seller_id, seller_name
    # and price from the sellers table and the product_sellers table. The result of the query is being
    # stored in the sellers variable.
    select_seller = """
        SELECT s.seller_id, seller_name, price
        FROM sellers s
        INNER JOIN product_sellers ps ON ps.seller_id = s.seller_id
        WHERE product_id = ?
        ORDER BY price
        """
    cursor.execute(
        select_seller,
        (product_id,),
    )
    sellers = cursor.fetchall()
    if sellers and len(sellers)==1:
        seller_id = sellers[0][0]
    elif sellers:
        seller_id = _display_options(sellers, "Sellers", "seller")
        # This is a for loop that is looping through the sellers variable. The if statement is
        # checking if the seller_id is in the seller variable. If it is, the product_price variable is
        # being set to the third item in the seller variable.
    if sellers:
        for seller in sellers:
            if seller_id in seller:
                product_price = seller[2]
        while True:
            try:
                quantiy = int(input("\nEnter the quantity you want to buy: "))
                break
            except ValueError:
                print("Please enter a valid quantity...")

        # This is a SQL query that is being executed. The query is selecting the basket_id from the
        # shopper_baskets table and ordering them by basket_id in descending order. The result of the query is
        # being stored in the basket_id variable.
        select_basket_id = """
        SELECT basket_id 
        FROM shopper_baskets
        ORDER BY basket_id DESC
        LIMIT 1
        """
        cursor.execute(select_basket_id)
        basket_id = cursor.fetchone()[0]

        # This is checking if the basket_id is empty. If it is, it is setting the basket_id to 1. If
        # it is not, it is adding 1 to the basket_id.
        if not basket_id:
            basket_id = 1
        else:
            basket_id += 1
        current_date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # This is a SQL query that is being executed. The query is inserting the basket_id, shopper_id
        # and basket_created_date_time into the shopper_baskets table. The result of the query is
        # being stored in the create_basket variable. The cursor is executing the create_basket
        # variable. 
        create_basket = """
                    INSERT INTO shopper_baskets(basket_id, shopper_id, basket_created_date_time)
                    VALUES (?, ?, ?)
                    """
        cursor.execute(
            create_basket,
            (
                basket_id,
                shopper_id,
                current_date_time,
            ),
        )
        db.commit()

        # This is a SQL query that is being executed. The query is inserting the basket_id,
        # product_id, seller_id, quantity and price into the basket_contents table. The result of the
        # query is being stored in the add_product variable. The cursor is executing the add_product
        # variable.
        add_product = """
                        INSERT INTO basket_contents(basket_id, product_id, seller_id, quantity, price)
                        VALUES (?, ?, ?, ?, ?)"""
        cursor.execute(
            add_product, (basket_id, product_id, seller_id, quantiy, product_price)
        )
        db.commit()
        print("\nItem added to the basket successfully!")

    else:
        print("No seller for this product!")


def _display_options(all_options, title, type):
    """
    It takes a list of lists, a title and a type, and displays the list of lists in a numbered list, and
    returns the selected item from the list of lists
    
    :param all_options: a list of tuples containing the options to display
    :param title: The title of the menu
    :param type: This is the type of option you want to display
    :return: The the option selected by the user.
    """
    option_num = 1
    option_list = []
    print("\n", title, "\n")
    for option in all_options:
        code = option[0]
        desc = option[1]
        if type == "seller":
            price = option[2]
            print("{0}. {1} (£{2})".format(option_num, desc, price))
            option_list.append(code)
        elif type == "address":
            print(
                "{0}. {1}, {2}, {3}, {4}, {5}".format(
                    option_num, desc, option[2], option[3] or "", option[4], option[5]
                )
            )
            option_list.append(code)
        elif type == "card":
            print("{0}. {1} ending in {2}".format(option_num, desc, option[2][-4:]))
            option_list.append(code)
        elif type == "card type":
            print("{0}. {1}".format(option_num, option))
            option_list.append(option)
        else:
            print("{0}. {1}".format(option_num, desc))
            option_list.append(code)
        option_num = option_num + 1
    selected_option = 0
    while selected_option > len(option_list) or selected_option == 0:
        prompt = "\nEnter the number against the " + type + " you want to choose: "
        while True:
            try:
                selected_option = int(input(prompt))
                break
            except ValueError:
                print("Please enter a valid number...")
    return option_list[selected_option - 1]
