def sql(db, cursor, shopper_id):
    cursor.execute(
    """
    SELECT sho.order_id AS [Order ID],
    STRFTIME('%d-%m-%Y', sho.order_date) AS [Order Date],
    p.product_description AS [Product Description],
    s.seller_name AS [Seller Name],
    PRINTF('£%0.2f', op.price) AS Price,
    op.quantity AS [Qty ordered],
    op.ordered_product_status AS [Order Status]
    FROM shoppers sh
    INNER JOIN shopper_orders sho ON sho.shopper_id = sh.shopper_id
    INNER JOIN ordered_products op ON op.order_id = sho.order_id
    INNER JOIN products p ON p.product_id = op.product_id
    INNER JOIN sellers s ON s.seller_id = op.seller_id
    WHERE sh.shopper_id = @shopper_id
    ORDER BY sho. order_date DESC 
    """,
        (shopper_id,),
    )
    results = cursor.fetchall()

    if results:
        print(
            "\n {0:10}   {1:10}   {2:70}    {3:20}  {4:10}   {5:10}    {6:10} ".format(
                "Order ID",
                "Order Date",
                "Product Description",
                "Seller",
                "Price",
                "Quantity",
                "Status",
            )
        )
        print("")
        for row in results:
            print(
                "{0:10}    {1:10}   {2:74} {3:20}  {4:10} {5:10}      {6:10} ".format(
                    row[0], row[1], row[2], row[3], row[4], row[5], row[6]
                )
            )
    else:
        print("\nNo orders placed by this customer.")
