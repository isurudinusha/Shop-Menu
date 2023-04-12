from datetime import datetime
from add_basket import _display_options
from view_basket import basket
from clear_basket import checkout_clear


def sql(db, cursor, shopper_id):
    if basket(db, cursor, shopper_id):
        # Selecting the delivery address from the database.
        select_address = """ 
        SELECT  da.delivery_address_id, delivery_address_line_1, delivery_address_line_2, delivery_address_line_3,delivery_county, delivery_post_code
        FROM shopper_delivery_addresses da
        INNER JOIN shopper_orders so ON so.delivery_address_id = da.delivery_address_id
        WHERE shopper_id = ?
        GROUP BY so.delivery_address_id
        ORDER BY da.delivery_address_id DESC
        """
        cursor.execute(
            select_address,
            (shopper_id,),
        )
        addresses = cursor.fetchall()
        if addresses and len(addresses) == 1:
            print(
                "Delivery address: {0}, {1}, {2}, {3}, {4}".format(
                    addresses[0][1],
                    addresses[0][2],
                    addresses[0][3] or "",
                    addresses[0][4],
                    addresses[0][5],
                )
            )
            address_id = addresses[0][0]
        elif addresses:
            address_id = _display_options(addresses, "Delivery Addresses", "address")
        else:
            print(
                "\nAs you have not yet placed any orders, you will need to enter a delivery address."
            )
            address_line_1 = input("\nEnter the delivery address line 1: ")
            address_line_2 = input("\nEnter the delivery address line 2: ")
            address_line_3 = input("\nEnter the delivery address line 3: ")
            country = input("\nEnter the delivery country: ")
            post_code = input("\nEnter the delivery post code: ")

            # This is a SQL query that inserts a new delivery address into the database.
            insert_address = """
            INSERT INTO shopper_delivery_addresses (delivery_address_line_1, delivery_address_line_2, delivery_address_line_3,
            delivery_county, delivery_post_code)
            VALUES(?, ?, ?, ?, ?)
            """

            cursor.execute(
                insert_address,
                (address_line_1, address_line_2, address_line_3, country, post_code),
            )
            db.commit()

            # This is a SQL query that selects the last delivery address from the database.
            select_new_address = """ 
            SELECT delivery_address_id
            FROM shopper_delivery_addresses 
            ORDER BY delivery_address_id DESC
            LIMIT 1
            """
            cursor.execute(select_new_address)
            address_id = cursor.fetchone()[0]

        # This is a SQL query that selects the payment card details from the database.
        select_payment = """        
        SELECT spc.payment_card_id, card_type, card_number
        FROM shopper_payment_cards spc
        INNER JOIN shopper_orders so ON so.payment_card_id = spc.payment_card_id
        WHERE so.shopper_id = ?
        GROUP BY spc.payment_card_id
        """
        cursor.execute(
            select_payment,
            (shopper_id,),
        )
        cards = cursor.fetchall()
        if cards and len(cards) == 1:
            print("Payments card: ", cards[0][1], "ending in", cards[0][2][-4:])
            card_id = cards[0][0]
        elif cards:
            card_id = _display_options(cards, "Payments cards", "card")
        else:
            print(
                "\nAs you have not yet placed any orders, you will need to enter your payment card details."
            )
            card_types = ["Visa", "Mastercard", "AMEX"]
            selected_card_type = _display_options(
                card_types, "Cards types", "card type"
            )

            card_number = 0
            while card_number == 0 or len(str(card_number)) != 16:
                card_number = input("Enter the 16 digits card number: ")

            # This is a SQL query that selects the last payment card from the database.
            select_last_card = """
            SELECT payment_card_id 
            FROM shopper_payment_cards 
            ORDER BY payment_card_id DESC
            LIMIT 1
            """
            cursor.execute(select_last_card)
            last_card_id = cursor.fetchone()[0]

            # This is a SQL query that inserts a new payment card into the database.
            insert_new_card = """
            INSERT INTO shopper_payment_cards(payment_card_id,  card_type, card_number)
            VALUES(?, ?, ?)
            """
            card_id = int(last_card_id) + 1
            cursor.execute(
                insert_new_card,
                (
                    card_id,
                    selected_card_type,
                    card_number,
                ),
            )
            db.commit()

        current_date = datetime.now().strftime("%Y-%m-%d")

        # This is a SQL query that selects the last order from the database.
        select_last_order = """
        SELECT order_id 
        FROM shopper_orders
        ORDER BY order_id DESC
        LIMIT 1
        """
        cursor.execute(select_last_order)
        last_order_id = cursor.fetchone()[0]
        new_order_id = int(last_order_id) + 1

        # This is a SQL query that inserts a new order into the database.
        insert_new_order = """
        INSERT INTO shopper_orders(order_id, shopper_id, delivery_address_id, payment_card_id, order_date, order_status)
        VALUES (?,?, ?, ?, ?, ?)
        """
        cursor.execute(
            insert_new_order,
            (new_order_id, shopper_id, address_id, card_id, current_date, "Placed"),
        )
        db.commit()

        # This is a SQL query that selects the product id, seller id, quantity and price from the
        # basket contents table.
        select_products_in_basket = """
        SELECT product_id, MAX(seller_id), SUM(quantity), SUM(price)
        FROM basket_contents bc
        INNER JOIN shopper_baskets  sb ON sb.basket_id = bc.basket_id
        WHERE sb.shopper_id = ?
        GROUP BY product_id
        """
        cursor.execute(
            select_products_in_basket,
            (shopper_id,),
        )
        products_in_basket = cursor.fetchall()

        if products_in_basket:
            for product in products_in_basket:

                # This is a SQL query that inserts a new order products into the database.
                ordered_products_query = """
                INSERT INTO ordered_products(order_id,product_id, seller_id, quantity, price, ordered_product_status)
                VALUES (?, ?, ?, ?, ?,?)
                """

                cursor.execute(
                    ordered_products_query,
                    (
                        new_order_id,
                        product[0],
                        product[1],
                        product[2],
                        product[3],
                        "Placed",
                    ),
                )
                db.commit()
            checkout_clear(db, cursor, shopper_id)
            print("\nCheckout complete, your order has been placed.")
        else:
            print("Error!")
