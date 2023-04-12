def basket(db, cursor, shopper_id):
        
    # Selecting the max product description, max seller name, sum of quantity, max price, and sum of
    # quantity * price from the basket contents table, shopper baskets table, product sellers table,
    # products table, and sellers table.
    select_basket = """ 
    SELECT MAX(product_description), MAX(seller_name), SUM(quantity), MAX(bc.price), SUM(quantity * bc.price)
    FROM basket_contents bc
    INNER JOIN shopper_baskets sb ON sb.basket_id = bc.basket_id
    INNER JOIN product_sellers ps ON ps.product_id = bc.product_id AND ps.seller_id = bc.seller_id
    INNER JOIN products p ON p.product_id = ps.product_id
    INNER JOIN sellers s ON s.seller_id = ps.seller_id
    WHERE sb.shopper_id = ?
    GROUP BY bc.product_id
    """

    cursor.execute(
        select_basket,
        (shopper_id,),
    )
    results = cursor.fetchall()
    total = 0
    if results:
        print("\nBasket Contents")
        print("-------------------")
        print(
            "\n {0:70}    {1:22}       {2:16}      {3:10}  {4:8}".format(
                "Product Description",
                "Seller Name",
                "Quantity",
                "Price",
                "Total",
            )
        )
        print("")
        for row in results:
            print(
                    " {0:70}    {1:24}   {2:10}         {3:10.2f}    {4:8.2f}".format(
                        row[0].strip(), row[1], row[2], row[3], row[4]
                    )
                )
            total += row[4]
        print("\n\t\t\t\t\t{0:67}Basket Total:  £{1:4.2f}".format(" ", total))
        return 1
    else:
        print("\nBasket is Empty\n")
        return 0

